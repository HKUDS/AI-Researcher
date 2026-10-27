# Resuming idea generation

Enable request checkpoints when starting the native idea workflow by adding
`--idea-checkpoint-dir /absolute/path/to/idea-checkpoints` to your usual
`research_agent/run_infer_idea.py` command. The directory must be new.

After an interruption, run the same command with the same checkpoint directory
and add `--resume-ideas`. Select **Yes** for the existing upstream preparation
caches so that the idea stage receives the same inputs. Each idea iteration and
the final selection has its own SQLite journal. Completed iterations restore
their messages, context and browser state; an interrupted iteration replays its
completed requests and sends the pending request again.

The checkpoint covers the idea agent's non-streaming chat completions, the paper
reader's chat completions, and OpenAI embedding responses used by paper memory.
Complete provider responses are committed before they are returned to the
caller, including responses with empty text. Tool outputs, retrieval results,
and the browser's page, navigation and search state are also persisted. This
keeps timing-dependent tool text and reader prompts identical during replay.
Each repeated call remains a separate occurrence, even when its request is
identical to an earlier call. Interrupted paper indexing finishes its remaining
batches even when earlier batches were already committed to Chroma.

Keep the same papers, prompts, model settings, Python environment and source
code when resuming. Changed inputs or requests stop replay rather than mixing
runs. API keys can be rotated; authentication headers and keys are excluded
from the journal. Checkpoints contain prompts, paper text and model responses,
so keep them with your other private run artifacts. Each journal is locked
against concurrent writers (Linux/macOS).

The flag applies to idea generation and selection. Preparation, code generation
and experiment execution retain their existing caches. Streaming requests are
not supported while an idea checkpoint is active. A response lost before its
local SQLite commit must be requested again. Existing runs without these
journals cannot be upgraded into request-level checkpoints.

For a custom driver using the same idea agent:

```python
from research_agent.inno.checkpoint import CheckpointedIdeaModule

idea = CheckpointedIdeaModule(agent, client, browser, "idea-checkpoints", resume=True)
messages, context = await idea(messages, context, iter_times=0)
```

Use `resume=False` for a new directory. Give each idea iteration a stable,
distinct `iter_times` value, and use the same values after restarting.

Run the offline tests in an installed project environment:

```bash
python -m unittest discover -s tests -p 'test_idea_checkpoint.py' -v
```

The tests kill a subprocess inside the native MetaChain loop, restart it, and
check that its output matches an uninterrupted run while completed API calls
and tools are not repeated. They also cover interruption inside a reader tool,
embedding replay after a committed Chroma insertion, changed-paper rejection,
independent repeated calls, incomplete responses and exclusive journal locks.
