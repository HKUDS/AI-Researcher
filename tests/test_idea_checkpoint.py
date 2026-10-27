"""Offline fault injection against the native MetaChain request loop."""
import asyncio
from functools import wraps
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

os.environ['LITELLM_LOCAL_MODEL_COST_MAP'] = 'True'
os.environ['DEFAULT_LOG'] = 'false'
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from research_agent.inno import MetaChain, Agent
from research_agent.inno import checkpoint as cp
from litellm import ModelResponse
from openai.types import CreateEmbeddingResponse


def response(content=None, tool=None):
    calls = None if tool is None else [{'id': tool[0], 'type': 'function', 'function': {
        'name': tool[1], 'arguments': json.dumps(tool[2])}}]
    return ModelResponse(choices=[{'index': 0, 'finish_reason': 'stop',
        'message': {'role': 'assistant', 'content': content, 'tool_calls': calls}}])


def append(path, value):
    with path.open('a') as f:
        f.write(json.dumps(value) + '\n')


def browser(directory):
    fields = dict(history=[['about:blank', 100]], page_title=None, viewport_current_page=0,
        viewport_pages=[[0, 0]], _page_content='', _find_on_page_query=None,
        _find_on_page_last_result=None, _current_page_path=None)
    return SimpleNamespace(**fields, local_workplace=str(directory),
                           retrieve_on_page=lambda question: 'Relevant text')


def child(directory, mode):
    checkpoint_dir = directory / 'journal'
    b = browser(directory)
    def open_paper(path: str):
        """Read a paper at path."""
        append(directory / 'tools.jsonl', 'open')
        b._current_page_path = path
        b._page_content = 'paper content'
        b.history.append([path, 123])
        return 'read at 123 seconds'
    def ask_reader(question: str):
        """Read the current paper and answer a question."""
        append(directory / 'tools.jsonl', 'reader')
        retrieved = b.retrieve_on_page(question)
        answer = cp.completion(model='test-reader', messages=[{'role':'user','content':retrieved}]).choices[0].message.content
        if mode == 'nested_interrupt':
            os._exit(92)
        return answer
    agent = Agent(name='Paper Survey Agent', model='test-model', instructions='Generate an idea',
                  functions=[open_paper, ask_reader], parallel_tool_calls=False)
    calls = 0
    async def provider(**kwargs):
        nonlocal calls
        append(directory / 'calls.jsonl', [mode, 'agent', kwargs])
        calls += 1
        if mode != 'resume':
            if calls == 1:
                return response(tool=('open', 'open_paper', {'path':'/papers/test.txt'}))
            if calls == 2:
                return response(tool=('reader', 'ask_reader', {'question':'Explain'}))
            if mode == 'interrupt':
                os._exit(91)
        return response('Final idea')
    def reader(**kwargs):
        append(directory / 'calls.jsonl', [mode, 'reader', kwargs])
        return response('Reader answer')
    module = cp.CheckpointedIdeaModule(agent, MetaChain(log_path=str(directory/'agent.log')),
                                     b, checkpoint_dir, resume=mode=='resume')
    with patch('litellm.acompletion', provider), patch('litellm.completion', reader):
        result = asyncio.run(module([{'role':'user','content':'Research task'}], {'notes':[]}))
    (directory/'output.json').write_text(json.dumps(result))
    (directory/'browser.json').write_text(json.dumps(cp.browser_state(b)))


class CheckpointTest(unittest.TestCase):
    def test_native_loop_cross_process_resume_matches_uninterrupted(self):
        with TemporaryDirectory() as tmp:
            base = Path(tmp)
            for name in ['baseline','resumed']:
                p = base/name; (p/'papers').mkdir(parents=True)
                (p/'papers/test.txt').write_text('paper content')
            command = [sys.executable, str(Path(__file__).resolve()), '--child']
            for directory, mode, code in [(base/'baseline','baseline',0),
                    (base/'resumed','interrupt',91),(base/'resumed','resume',0)]:
                result = subprocess.run(command+[str(directory),mode], capture_output=True,text=True)
                self.assertEqual(result.returncode,code,result.stdout+result.stderr)
            self.assertEqual((base/'baseline/output.json').read_bytes(), (base/'resumed/output.json').read_bytes())
            self.assertEqual((base/'baseline/browser.json').read_bytes(), (base/'resumed/browser.json').read_bytes())
            calls=[json.loads(line) for line in (base/'resumed/calls.jsonl').read_text().splitlines()]
            self.assertEqual([(c[0],c[1]) for c in calls], [('interrupt','agent'),('interrupt','agent'),
                ('interrupt','reader'),('interrupt','agent'),('resume','agent')])
            self.assertEqual(calls[-1][2],calls[-2][2])
            self.assertEqual(len((base/'resumed/tools.jsonl').read_text().splitlines()),2)
            result=subprocess.run(command+[str(base/'resumed'),'resume'],capture_output=True,text=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(len((base/'resumed/calls.jsonl').read_text().splitlines()),5)

    def test_crash_inside_reader_reuses_retrieval_and_reader_response(self):
        with TemporaryDirectory() as tmp:
            directory = Path(tmp)
            command = [sys.executable, str(Path(__file__).resolve()), '--child', str(directory)]
            first = subprocess.run(command + ['nested_interrupt'], capture_output=True, text=True)
            self.assertEqual(first.returncode, 92, first.stdout + first.stderr)
            second = subprocess.run(command + ['resume'], capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stdout + second.stderr)
            calls = [json.loads(line) for line in (directory/'calls.jsonl').read_text().splitlines()]
            self.assertEqual([(c[0], c[1]) for c in calls], [('nested_interrupt', 'agent'),
                ('nested_interrupt', 'agent'), ('nested_interrupt', 'reader'), ('resume', 'agent')])

    def test_disabled_checkpoint_passes_requests_through(self):
        with patch('litellm.completion', return_value='stream') as sync, \
                patch('litellm.acompletion', return_value='async-stream') as asynchronous:
            self.assertEqual(cp.completion(stream=True), 'stream')
            self.assertEqual(asyncio.run(cp.acompletion(stream=True)), 'async-stream')
            sync.assert_called_once_with(stream=True)
            asynchronous.assert_called_once_with(stream=True)

    def test_native_browser_reader_restores_memory_and_reuses_retrieval(self):
        # Stub only optional converter/storage dependencies. Execute the upstream
        # browser and reader methods, without installing OCR or downloading models.
        package = 'research_agent.inno.environment.markdown_browser'
        base = ROOT/'research_agent/inno/environment/markdown_browser'
        modules = {}
        for name in [package, package+'.markdown_search', package+'.mdconvert', 'inno.memory.paper_memory']:
            modules[name] = ModuleType(name)
        modules[package].__path__ = [str(base)]
        for name in ['AbstractMarkdownSearch', 'BingMarkdownSearch']:
            setattr(modules[package+'.markdown_search'], name, object)
        for name in ['FileConversionException', 'UnsupportedFormatException', 'MarkdownConverter']:
            setattr(modules[package+'.mdconvert'], name, object)
        modules['inno.memory.paper_memory'].PaperMemory = object
        from research_agent import constant
        modules['constant'] = constant
        with patch.dict(sys.modules, modules), TemporaryDirectory() as tmp:
            spec = importlib.util.spec_from_file_location(package+'.requests_markdown_browser', base/'requests_markdown_browser.py')
            native = importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
            modules[package].RequestsMarkdownBrowser = native.RequestsMarkdownBrowser
            spec = importlib.util.spec_from_file_location('checkpoint_test_reader', ROOT/'research_agent/inno/tools/file_surfer_tool.py')
            reader = importlib.util.module_from_spec(spec);spec.loader.exec_module(reader)
            directory=Path(tmp)
            retrievals=[]
            class Memory:
                def count(self, collection): return 1
                def query_paper_content(self, **kwargs):
                    retrievals.append(kwargs)
                    return ['relevant native browser result']
            async def run(resume):
                b=native.RequestsMarkdownBrowser.__new__(native.RequestsMarkdownBrowser)
                for key,value in vars(browser(directory)).items():
                    if key != 'retrieve_on_page':setattr(b,key,value)
                b._current_page_path='/papers/test.txt';b._page_content='paper';b._memory=Memory()
                b.docker_workplace='/workplace';b.viewport_size=8192
                fn=reader.with_env(b)(reader.question_answer_on_whole_page)
                agent=Agent(name='Reader',model='test',instructions='Read',functions=[fn])
                class Client:
                    async def run_async(self, agent, messages, **kwargs):
                        answer=agent.functions[0](question='Explain')
                        return SimpleNamespace(messages=[{'role':'assistant','content':answer}],context_variables={})
                module=cp.CheckpointedIdeaModule(agent,Client(),b,directory/'journal',resume=resume)
                return await module([], {})
            with patch('litellm.completion',side_effect=ConnectionError('interrupted')):
                with self.assertRaises(cp.RequestInterrupted):asyncio.run(run(False))
            with patch('litellm.completion',return_value=response('answer')) as backend:
                result=asyncio.run(run(True))
                self.assertEqual(result[0][-1]['content'],'answer')
                self.assertIn('relevant native browser result',str(backend.call_args))
            self.assertEqual(len(retrievals),1)

    def test_occurrences_mismatch_and_owner_lock(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/'journal.sqlite3'
            journal=cp.Journal(path)
            for value in ['one','two']:
                slot,_=journal.begin({'model':'same'});journal.finish(slot,{'value':value})
            with self.assertRaises(RuntimeError): cp.Journal(path)
            journal.close()
            journal=cp.Journal(path)
            self.assertEqual(journal.begin({'model':'same'})[1],{'value':'one'})
            with self.assertRaises(cp.ResumeMismatch):journal.begin({'model':'changed'})
            journal.close()

    def test_reader_failure_escapes_error_to_string_and_resends(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/'journal.sqlite3'
            for failure in [True,False]:
                journal=cp.Journal(path);token=cp._active_journal.set(journal)
                with patch('litellm.completion') as backend:
                    if failure:backend.side_effect=ConnectionError('interrupted')
                    else:backend.return_value=response('answer')
                    try:
                        if failure:
                            with self.assertRaises(cp.RequestInterrupted):cp.completion(model='reader')
                        else:self.assertEqual(cp.completion(model='reader').choices[0].message.content,'answer')
                    finally:cp._active_journal.reset(token);journal.close()
                    self.assertEqual(backend.call_count,1)

    def test_embedding_replay_after_chroma_insertion_was_committed(self):
        with TemporaryDirectory() as tmp:
            path=Path(tmp)/'journal.sqlite3'
            client=SimpleNamespace(base_url='https://test.invalid', embeddings=SimpleNamespace(create=None))
            def embedding(**kwargs):
                return CreateEmbeddingResponse(data=[{'embedding':[1.,2.], 'index':0,'object':'embedding'}],
                    model='embedding-model',object='list',usage={'prompt_tokens':1,'total_tokens':1})
            for phase in ['initial','resume']:
                journal=cp.Journal(path);token=cp._active_journal.set(journal)
                with patch.object(client.embeddings,'create',side_effect=embedding) as backend:
                    if phase=='initial':cp.embedding_create(client,model='embedding-model',input=['paper'])
                    cp.embedding_create(client,model='embedding-model',input=['query'])
                    self.assertEqual(backend.call_count,2 if phase=='initial' else 0)
                cp._active_journal.reset(token);journal.close()

    def test_second_embedding_batch_failure_finishes_partial_paper_index(self):
        # Run the native PaperMemory batching code; replace only Chroma storage
        # and token splitting, so a small fixture exercises its 100-chunk boundary.
        requests = []
        fail = True
        def create(**kwargs):
            requests.append(kwargs)
            if fail and len(requests) == 2:
                raise ConnectionError('second batch interrupted')
            return CreateEmbeddingResponse(data=[{'embedding':[float(i)], 'index':i,
                'object':'embedding'} for i in range(len(kwargs['input']))],
                model='embedding-model',object='list',usage={'prompt_tokens':1,'total_tokens':1})
        client=SimpleNamespace(base_url='https://test.invalid',embeddings=SimpleNamespace(create=create))
        class Storage:
            def __init__(self, **kwargs): self.rows = {}
            def count(self, collection): return len(self.rows)
            def add_query(self, queries, collection, idx):
                cp.embedding_create(client,model='embedding-model',input=[q['query'] for q in queries])
                for key,row in zip(idx,queries):self.rows.setdefault(key,row)
        dependency=ModuleType('research_agent.inno.memory.rag_memory')
        dependency.Memory=Storage;dependency.Reranker=object
        with patch.dict(sys.modules, {'research_agent.inno.memory.rag_memory':dependency}):
            spec=importlib.util.spec_from_file_location('checkpoint_test_paper_memory',
                ROOT/'research_agent/inno/memory/paper_memory.py')
            native=importlib.util.module_from_spec(spec);spec.loader.exec_module(native)
        memory=native.PaperMemory(project_path='unused')
        chunks=[{'chunk_order_index':i,'content':f'chunk {i}'} for i in range(101)]
        with TemporaryDirectory() as tmp, patch.object(native,'chunking_by_token_size',return_value=chunks):
            path=Path(tmp)/'journal.sqlite3'
            for phase in ['interrupt','resume','completed']:
                journal=cp.Journal(path);token=cp._active_journal.set(journal)
                try:
                    if phase=='interrupt':
                        with self.assertRaises(cp.RequestInterrupted):cp.ensure_paper_index(memory,'paper','content')
                        self.assertEqual(memory.count('paper'),100)
                    else:
                        fail=False
                        cp.ensure_paper_index(memory,'paper','content')
                        self.assertEqual(memory.count('paper'),101)
                finally:cp._active_journal.reset(token);journal.close()
            self.assertEqual([len(r['input']) for r in requests],[100,1,1])
            self.assertEqual(requests[1],requests[2])

    def test_incomplete_response_pending_and_credentials_not_persisted(self):
        with TemporaryDirectory() as tmp:
            journal=cp.Journal(Path(tmp)/'journal.sqlite3');token=cp._active_journal.set(journal)
            partial=response('partial');partial.choices[0].finish_reason=None
            try:
                with patch('litellm.completion',return_value=partial):
                    with self.assertRaises(cp.RequestInterrupted):
                        cp.completion(model='reader',api_key='secret-value',extra_headers={'Authorization':'secret-value','X-Route':'r1'})
                request,payload=journal.db.execute('SELECT request,response FROM events').fetchone()
                self.assertIsNone(payload);self.assertNotIn('secret-value',request);self.assertIn('X-Route',request)
            finally:cp._active_journal.reset(token);journal.close()

    def test_changed_paper_refuses_completed_stage(self):
        with TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'papers').mkdir();paper=p/'papers/test.txt';paper.write_text('initial')
            child(p,'baseline');paper.write_text('modified')
            with self.assertRaises(cp.ResumeMismatch):child(p,'resume')


if __name__=='__main__':
    if '--child' in sys.argv:child(Path(sys.argv[-2]),sys.argv[-1])
    else:unittest.main()
