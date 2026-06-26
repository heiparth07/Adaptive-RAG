# Testing — Adaptive RAG

A hermetic, CI-ready test suite for the Adaptive RAG pipeline. Every external
boundary (the LLM, the compiled LangGraph, MongoDB, document ingestion / vector
store) is mocked, so the whole suite runs **with no API keys, no database, and
no network** — locally and on every push.

```bash
pip install -r requirements-test.txt
pytest
```
→ **38 passed, 2 skipped** in well under a second.

## Why it's built this way
LLM systems are non-deterministic, call paid APIs, and depend on external
services — so a naive "spin up the whole pipeline and assert the answer" suite is
slow, flaky, expensive, and needs secrets. Instead this suite:

- **Mocks every external boundary** in `conftest.py` (LLM client, compiled
  graph, Mongo chat history, document ingestion) by injecting fakes into
  `sys.modules` *before* the app imports them. The suite is fully deterministic.
- **Tests the real logic** that actually has behaviour worth verifying: the
  routing/grading control flow, the request/response contract and its
  validation, and the structured-output schemas.
- **Separates fast unit tests from slow live tests.** The hermetic suite gates
  every commit; an optional live suite (real LLM, real key) runs on demand.

## What's covered (40 tests)

| File | Tests | What it verifies |
|------|------:|------------------|
| `tests/test_models.py` | 12 | Pydantic schemas — the request contract (`QueryRequest`) and the structured-output models that make the LLM's output testable (`Grade`, `RouteIdentifier`, `VerificationResult`). |
| `tests/test_routing_logic.py` | 7 | The graph's deterministic decision points: `routing_tool` (intent routing → retriever / general LLM / web search) and `doc_tool` (the corrective loop → generate vs rewrite). |
| `tests/test_api.py` | 12 | The real FastAPI routes via `TestClient`: health/root, the `/rag/query` contract and its validation (empty, whitespace, over-length, boundary, missing field), session clear, and document upload. |
| `tests/test_eval_set.py` | 7 | An **evals-as-CI** harness: a versioned dataset of routing cases run as a regression gate, plus an aggregate pass-rate threshold check. |
| `tests/test_live_optional.py` | 2 | Optional live faithfulness checks against the real LLM. **Skipped by default.** |

## Running

```bash
# Hermetic suite (default — no keys needed)
pytest

# Verbose
pytest -v

# Only the routing logic
pytest tests/test_routing_logic.py

# Optional LIVE tests (real LLM, costs money, non-deterministic)
RUN_LIVE_TESTS=1 OPENAI_API_KEY=sk-... pytest -m live
```

## The testing strategy, in layers
This mirrors the test pyramid applied to an AI pipeline:

1. **Schema / unit** — models and pure decision logic. Fast, exhaustive, deterministic.
2. **API / integration** — real route handlers with mocked collaborators; validates the contract and input handling.
3. **Evaluation set** — dataset-driven regression for pipeline *behaviour*, with
   aggregate thresholds rather than single-run assertions — the right shape for a
   probabilistic system. Grows by adding rows (including edge/adversarial cases
   found in production) so it runs on every prompt / model / routing change.
4. **Live (optional)** — real end-to-end checks behind a flag, kept out of the
   per-commit path.

## Extending the eval set
Add a case to `EVAL_CASES` in `tests/test_eval_set.py` — one row per scenario,
each pairing an input with an **expected property** (not a frozen string). For
LLM-judged dimensions like faithfulness or answer relevancy, score the set and
gate on a threshold (e.g. `>= 0.9`) instead of requiring every case to pass in
isolation.

## CI
`.github/workflows/tests.yml` installs `requirements-test.txt` and runs `pytest`
on every push and pull request. Because the suite is hermetic, **CI needs no
secrets and none of the heavy ML dependencies** (faiss / qdrant / openai / motor).
