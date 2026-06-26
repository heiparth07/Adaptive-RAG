"""
Routing and grading decision-logic tests.

`routing_tool` and `doc_tool` are the deterministic decision points of the
Adaptive RAG graph:

  - routing_tool  -> sends a classified query to retrieval, the general LLM,
                     or web search   (this is "intent routing")
  - doc_tool      -> after grading retrieved docs, either generates the answer
                     or rewrites the query and retries  (the corrective loop)

They're pure functions of the graph state, so we can test the control flow
exhaustively and deterministically — no LLM required.
"""

import pytest

from src.tools.graph_tools import routing_tool, doc_tool


class TestRoutingTool:
    """Intent routing: query classification -> next node."""

    def test_index_route_goes_to_retriever(self):
        assert routing_tool({"route": "index"}) == "retriever"

    def test_general_route_goes_to_general_llm(self):
        assert routing_tool({"route": "general"}) == "general_llm"

    def test_web_route_goes_to_web_search(self):
        assert routing_tool({"route": "web"}) == "web_search"

    def test_unknown_route_falls_back_to_web_search(self):
        # Anything that isn't 'index' or 'general' should fall back to web.
        assert routing_tool({"route": "something_unexpected"}) == "web_search"


class TestDocTool:
    """Corrective loop: document-relevance grade -> generate or rewrite."""

    def test_relevant_docs_proceed_to_generate(self):
        assert doc_tool({"binary_score": "yes"}) == "generate"

    def test_irrelevant_docs_trigger_rewrite(self):
        assert doc_tool({"binary_score": "no"}) == "rewrite"

    def test_non_yes_score_triggers_rewrite(self):
        # Only an explicit "yes" should proceed; everything else rewrites.
        assert doc_tool({"binary_score": "maybe"}) == "rewrite"
