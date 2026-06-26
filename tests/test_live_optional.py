"""
Optional LIVE / integration tests.

Everything else in this suite is hermetic and runs with no keys. These tests
are the opposite: they exercise the real LLM end-to-end and therefore need a
real OPENAI_API_KEY (and cost money / are non-deterministic). They are SKIPPED
BY DEFAULT.

To run them:
    RUN_LIVE_TESTS=1 OPENAI_API_KEY=sk-... pytest -m live

Keeping fast, deterministic unit tests separate from slow, paid, live tests is
deliberate: the unit suite gates every commit; the live suite runs on demand.
"""

import os

import pytest

pytestmark = pytest.mark.live

run_live = os.getenv("RUN_LIVE_TESTS") == "1"
skip_reason = "Live tests disabled. Set RUN_LIVE_TESTS=1 and OPENAI_API_KEY to run."


@pytest.mark.skipif(not run_live, reason=skip_reason)
def test_grounded_answer_is_faithful():
    """
    A grounded answer should be judged faithful by the verifier.

    This is a property-based check against a real LLM: we don't assert an exact
    string, we assert that an answer supported by the context passes the
    faithfulness verifier. (Implementation intentionally left to wire up against
    the live verifier so the hermetic suite stays import-clean.)
    """
    pytest.skip("Template: wire up against the live verify_answer flow with a real key.")


@pytest.mark.skipif(not run_live, reason=skip_reason)
def test_fabricated_answer_is_flagged():
    """A claim NOT supported by the context should be flagged as not faithful."""
    pytest.skip("Template: wire up against the live verify_answer flow with a real key.")
