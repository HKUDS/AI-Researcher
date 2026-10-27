"""Durable request and browser-tool replay for the sequential ideation agent."""
from contextvars import ContextVar
from functools import wraps
import json
from pathlib import Path
import sqlite3
import threading


class RequestInterrupted(BaseException):
    """Escape tool wrappers that otherwise turn failed API calls into text."""


class ResumeMismatch(RequestInterrupted):
    """Stop replay immediately rather than letting an agent handle a changed request."""


class Journal:
    def __init__(self, path):
        import fcntl
        self._fcntl = fcntl
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.lock_file = self.path.with_suffix('.lock').open('a')
        try:
            fcntl.flock(self.lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self.lock_file.close()
            raise RuntimeError('This run is already active') from None
        self.db = sqlite3.connect(self.path, check_same_thread=False)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS events (scope TEXT, position INTEGER, request TEXT, response TEXT, PRIMARY KEY(scope, position))')
        self.db.commit()
        self.cursors = {}
        self.mutex = threading.RLock()
        self.scope = ContextVar('request_scope', default='agent')
        self.replayed = 0
        self.sent = 0

    @staticmethod
    def encode(value):
        return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False)

    def begin(self, request, scope=None):
        scope = scope or self.scope.get()
        payload = self.encode(request)
        with self.mutex:
            position = self.cursors.get(scope, 0)
            row = self.db.execute('SELECT request,response FROM events WHERE scope=? AND position=?', (scope, position)).fetchone()
            if row is not None and row[0] != payload:
                raise ResumeMismatch(f'Request changed at {scope}/{position}; use a new run directory')
            if row is None:
                self.db.execute('INSERT INTO events VALUES (?,?,?,NULL)', (scope, position, payload))
                self.db.commit()
            if row is not None and row[1] is not None:
                self.cursors[scope] = position + 1
                self.replayed += 1
                return (scope, position), json.loads(row[1])
            return (scope, position), None

    def finish(self, slot, response):
        encoded = self.encode(response)
        with self.mutex:
            self.db.execute('UPDATE events SET response=? WHERE scope=? AND position=?', (encoded, *slot))
            self.db.commit()
            self.cursors[slot[0]] = slot[1] + 1
            self.sent += 1

    def close(self):
        self.db.close()
        self._fcntl.flock(self.lock_file, self._fcntl.LOCK_UN)
        self.lock_file.close()


_BROWSER_FIELDS = ('history', 'page_title', 'viewport_current_page', 'viewport_pages',
                   '_page_content', '_find_on_page_query', '_find_on_page_last_result',
                   '_current_page_path')


def journal_tools(agent, browser, journal):
    def wrap(function):
        @wraps(function)
        def call(*args, **kwargs):
            slot, cached = journal.begin({'name': function.__name__, 'args': args, 'kwargs': kwargs}, 'tools')
            if cached is not None:
                for name, value in cached['browser'].items():
                    setattr(browser, name, value)
                return cached['result']
            token = journal.scope.set(f'tool/{slot[1]}')
            try:
                result = function(*args, **kwargs)
            finally:
                journal.scope.reset(token)
            state = browser_state(browser)
            journal.finish(slot, {'result': result, 'browser': state})
            return result
        return call
    agent.functions = [wrap(function) for function in agent.functions]


def browser_state(browser):
    return {name: getattr(browser, name) for name in _BROWSER_FIELDS}


def restore_browser(browser, state):
    for name, value in state.items():
        setattr(browser, name, value)


_active_journal = ContextVar("idea_request_journal", default=None)


def _request(kwargs):
    # Authentication may be rotated between attempts and is never journaled.
    result = {key: value for key, value in kwargs.items()
              if key not in {"api_key", "api_token", "authorization"}}
    for field in ("headers", "extra_headers"):
        if isinstance(result.get(field), dict):
            result[field] = {key: value for key, value in result[field].items()
                             if key.lower() not in {"authorization", "api-key", "x-api-key"}}
    return result


def _save_response(journal, slot, result):
    payload = result.model_dump()
    if not payload.get("choices") or any(c.get("finish_reason") is None for c in payload["choices"]):
        raise RequestInterrupted("Incomplete API response; resume to resend the pending request")
    journal.finish(slot, payload)
    return result


async def acompletion(**kwargs):
    import litellm
    journal = _active_journal.get()
    if journal is None:
        return await litellm.acompletion(**kwargs)
    if kwargs.get("stream"):
        raise RequestInterrupted("Idea checkpoints require non-streaming completions")
    slot, cached = journal.begin(_request(kwargs))
    if cached is not None:
        return litellm.ModelResponse(**cached)
    # Preserve MetaChain's existing retry policy for agent requests.
    result = await litellm.acompletion(**kwargs)
    return _save_response(journal, slot, result)


def completion(**kwargs):
    import litellm
    journal = _active_journal.get()
    if journal is None:
        return litellm.completion(**kwargs)
    if kwargs.get("stream"):
        raise RequestInterrupted("Idea checkpoints require non-streaming completions")
    slot, cached = journal.begin(_request(kwargs))
    if cached is not None:
        return litellm.ModelResponse(**cached)
    try:
        result = litellm.completion(**kwargs)
    except Exception as exc:
        # Reader tools normally turn exceptions into strings; leave this call pending.
        raise RequestInterrupted("Reader request failed; resume to resend it") from exc
    return _save_response(journal, slot, result)


class CheckpointedIdeaModule:
    """AgentModule-compatible replay for the read-only paper ideation stage."""

    def __init__(self, agent, client, browser, checkpoint_dir, resume=False):
        self.agent, self.client, self.browser = agent, client, browser
        self.directory = Path(checkpoint_dir)
        if not resume:
            self.directory.mkdir(parents=True, exist_ok=False)
        elif not self.directory.is_dir():
            raise ValueError("Idea checkpoint directory does not exist")
        self.resume = resume

    async def __call__(self, messages, context_variables, iter_times=None, **kwargs):
        import copy
        import hashlib
        import sys
        from importlib.metadata import version
        from .util import function_to_json
        from research_agent import constant
        name = 'initial' if iter_times is None else str(iter_times)
        if Path(name).name != name or name in {'.', '..'}:
            raise ValueError("Invalid idea iteration name")
        path = self.directory / (name + '.sqlite3')
        if path.exists() and not self.resume:
            raise ValueError("Idea iteration already exists; use resume or a new directory")
        journal = Journal(path)
        functions = self.agent.functions
        original_retrieve = self.browser.retrieve_on_page
        token = _active_journal.set(journal)
        try:
            papers = Path(self.browser.local_workplace) / 'papers'
            instructions = self.agent.instructions(context_variables) if callable(self.agent.instructions) else self.agent.instructions
            source = Path(__file__).parent
            code_digest = hashlib.sha256()
            for file in sorted(source.rglob('*.py')):
                code_digest.update(str(file.relative_to(source)).encode())
                code_digest.update(file.read_bytes())
            identity = {'source': code_digest.hexdigest(), 'python': sys.version,
                        'dependencies': {p: version(p) for p in ('litellm', 'openai', 'pydantic')},
                        'reader_model': constant.COMPLETION_MODEL, 'base_url': constant.API_BASE_URL,
                        'model': self.agent.model, 'instructions': instructions,
                        'examples': self.agent.examples(context_variables) if callable(self.agent.examples) else self.agent.examples,
                        'tool_choice': self.agent.tool_choice, 'parallel_tool_calls': self.agent.parallel_tool_calls,
                        'completion_options': kwargs,
                        'browser_settings': {k: getattr(self.browser, k, None) for k in
                                             ('viewport_size', 'docker_workplace', 'local_workplace')},
                        'tools': [function_to_json(f) for f in functions],
                        'messages': messages, 'context_variables': context_variables,
                        'papers': {str(p.relative_to(papers)): hashlib.sha256(p.read_bytes()).hexdigest()
                                   for p in sorted(papers.rglob('*')) if p.is_file()}}
            # The entry state is committed before the first API call. Time-bearing browser
            # fields are restored rather than compared across process restarts.
            slot, entry = journal.begin(identity, 'entry')
            if entry is None:
                entry = {'browser': browser_state(self.browser)}
                journal.finish(slot, entry)
            restore_browser(self.browser, entry['browser'])
            slot, completed = journal.begin({'stage': name}, 'result')
            if completed is None:
                journal_tools(self.agent, self.browser, journal)
                def retrieve(question):
                    request = {'question': question, 'page': self.browser._current_page_path}
                    key, cached = journal.begin(request, journal.scope.get() + '/retrieval')
                    if cached is not None:
                        return cached['result']
                    try:
                        result = original_retrieve(question)
                    except Exception as exc:
                        raise RequestInterrupted('Paper retrieval failed; resume this run') from exc
                    journal.finish(key, {'result': result})
                    return result
                self.browser.retrieve_on_page = retrieve
                response = await self.client.run_async(self.agent, copy.deepcopy(messages),
                    context_variables=copy.deepcopy(context_variables), debug=True, **kwargs)
                if not response.messages or response.messages[-1]['role'] == 'error':
                    raise RequestInterrupted('Idea agent interrupted; resume this checkpoint directory')
                completed = {'messages': response.messages, 'context_variables': response.context_variables,
                             'browser': browser_state(self.browser)}
                journal.finish(slot, completed)
            restore_browser(self.browser, completed['browser'])
            messages.extend(completed['messages'])
            context_variables.update(completed['context_variables'])
            return messages, context_variables
        finally:
            self.agent.functions = functions
            self.browser.retrieve_on_page = original_retrieve
            _active_journal.reset(token)
            journal.close()


def embedding_create(client, **kwargs):
    """Persist the complete OpenAI embedding response before Chroma consumes it."""
    import hashlib
    from openai.types import CreateEmbeddingResponse
    journal = _active_journal.get()
    if journal is None:
        return client.embeddings.create(**kwargs)
    request = {'base_url': str(client.base_url), **_request(kwargs)}
    # Chroma may already contain an insertion committed before interruption. Key
    # embedding calls independently so skipping that insertion does not shift a query.
    digest = hashlib.sha256(journal.encode(request).encode()).hexdigest()
    slot, cached = journal.begin(request, journal.scope.get() + '/embedding/' + digest)
    if cached is not None:
        return CreateEmbeddingResponse(**cached)
    try:
        result = client.embeddings.create(**kwargs)
    except Exception as exc:
        raise RequestInterrupted('Embedding request failed; resume to resend it') from exc
    journal.finish(slot, result.model_dump())
    return result


def ensure_paper_index(memory, collection, content):
    """Finish every indexing batch even if an earlier batch reached Chroma."""
    import hashlib
    journal = _active_journal.get()
    if journal is None:
        if memory.count(collection) == 0:
            memory.add_paper_content(paper_content=content, collection=collection)
        return
    request = {'collection': collection, 'content_sha256': hashlib.sha256(content.encode()).hexdigest()}
    scope = journal.scope.get() + '/index'
    slot, decision = journal.begin(request, scope)
    if decision is None:
        decision = {'needed': memory.count(collection) == 0}
        journal.finish(slot, decision)
    slot, completed = journal.begin({'index': request}, scope)
    if completed is None:
        if decision['needed']:
            # PaperMemory uses stable chunk IDs. Replaying committed batches is
            # idempotent in Chroma and their embedding responses are journaled.
            memory.add_paper_content(paper_content=content, collection=collection)
        journal.finish(slot, {'complete': True})
