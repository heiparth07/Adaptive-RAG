"""
Evaluation-set harness (the seed of "evals-as-CI").

This is the pattern for regression-testing an LLM pipeline's behaviour: keep a
*versioned dataset* of cases, each with an input and an EXPECTED PROPERTY (not a
frozen output string), and run the whole set on every commit. When a prompt,
model, or routing change regresses a case, the build fails.

Here we evaluate the routing layer deterministically: given how a query was
classified, did control flow land on the correct node? Growing this suite is as
simple as adding rows to EVAL_CASES — including the edge and adversarial cases
you discover in production.
"""

import pytest

from src.tools.graph_tools import routing_tool

# (case_id, classified_route, expected_node)
EVAL_CASES = [
    ("kb_lookup_pet_policy",        "index",   "retriever"),
    ("kb_lookup_account_balance",   "index",   "retriever"),
    ("chitchat_greeting",           "general", "general_llm"),
    ("general_knowledge_question",  "general", "general_llm"),
    ("current_events_latest_news",  "web",     "web_search"),
    ("ambiguous_defaults_to_web",   "unknown", "web_search"),
]


@pytest.mark.parametrize(
    "case_id, classified_route, expected_node",
    EVAL_CASES,
    ids=[c[0] for c in EVAL_CASES],
)
def test_routing_eval_set(case_id, classified_route, expected_node):
    """Each case must route to its expected node — regression gate for routing."""
    assert routing_tool({"route": classified_route}) == expected_node


def test_eval_set_pass_rate_threshold():
    """
    Aggregate threshold check — the way you grade a probabilistic system.

    Instead of requiring every case to pass in isolation, we score the whole
    set and require the pass rate to clear a threshold (here, 100% because the
    routing layer is deterministic; for LLM-judged metrics like faithfulness
    you'd set something like >= 0.9).
    """
    passed = sum(
        routing_tool({"route": route}) == expected
        for _, route, expected in EVAL_CASES
    )
    pass_rate = passed / len(EVAL_CASES)
    assert pass_rate >= 0.9, f"Routing eval pass rate {pass_rate:.2f} below threshold"
