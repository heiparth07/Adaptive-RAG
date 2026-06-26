"""
Shared pytest fixtures and test setup for the Adaptive RAG test suite.

These tests are *hermetic*: every external boundary (the LLM, the compiled
LangGraph pipeline, MongoDB chat history, and document ingestion / vector store)
is replaced with a lightweight fake here, BEFORE the application is imported.

That means the whole suite runs with:
  - no API keys (OpenAI / Tavily / Groq)
  - no running MongoDB
  - no vector store or network calls

...which makes it safe to run locally and in CI on every push.
"""

import os
import sys
import types
from unittest.mock import MagicMock

import pytest

# ---------------------------------------------------------------------------
# 1. Dummy environment so any client instantiation stays offline-safe.
# ---------------------------------------------------------------------------
os.environ.setdefault("OPENAI_API_KEY", "test-key")
os.environ.setdefault("TAVILY_API_KEY", "test-key")
os.environ.setdefault("GROQ_API_KEY", "test-key")
os.environ.setdefault("LLM_PROVIDER", "openai")

# ---------------------------------------------------------------------------
# 2. Fake the external-service boundaries BEFORE the app imports them.
#    We inject fake modules into sys.modules so that `from X import Y` in the
#    application picks up our fakes instead of the real (heavy) modules.
# ---------------------------------------------------------------------------

# 2a. LLM client -> a MagicMock (no real model, no key needed).
_fake_llm_mod = types.ModuleType("src.llms.llm")
_fake_llm_mod.llm = MagicMock(name="llm")
sys.modules["src.llms.llm"] = _fake_llm_mod

# 2b. Compiled LangGraph pipeline -> deterministic canned answer.
from langchain_core.messages import AIMessage  # noqa: E402  (after env setup)

_fake_graph_builder = types.ModuleType("src.rag.graph_builder")
_builder = MagicMock(name="builder")
_builder.invoke.return_value = {"messages": [AIMessage(content="mocked answer")]}
_fake_graph_builder.builder = _builder
sys.modules["src.rag.graph_builder"] = _fake_graph_builder

# 2c. Document ingestion / vector store -> no-op that reports success.
_fake_document_upload = types.ModuleType("src.rag.document_upload")
_fake_document_upload.documents = MagicMock(name="documents", return_value=True)
sys.modules["src.rag.document_upload"] = _fake_document_upload

# 2d. MongoDB-backed chat history -> in-memory no-op.
_fake_chat_history = types.ModuleType("src.memory.chat_history_mongo")


class _FakeHistory:
    """In-memory stand-in for MongoDBChatMessageHistory."""

    def __init__(self, session_id="session"):
        self.session_id = session_id

    async def add_message(self, message):
        return None

    async def get_messages(self):
        return []

    async def clear(self):
        return None


class _FakeChatHistory:
    """Stand-in factory matching ChatHistory.get_session_history()."""

    @classmethod
    def get_session_history(cls, session_id, config=None):
        return _FakeHistory(session_id)


_fake_chat_history.ChatHistory = _FakeChatHistory
sys.modules["src.memory.chat_history_mongo"] = _fake_chat_history


# ---------------------------------------------------------------------------
# 3. Fixtures
# ---------------------------------------------------------------------------
@pytest.fixture
def client():
    """A FastAPI TestClient with all external boundaries mocked."""
    from fastapi.testclient import TestClient

    from src.main import app

    return TestClient(app)


@pytest.fixture
def mock_builder():
    """Direct handle on the fake graph builder (to assert/override per-test)."""
    return _builder
