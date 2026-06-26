"""
Schema / data-model tests.

These validate the real Pydantic models used across the RAG pipeline:
the request contract (QueryRequest) and the three structured-output schemas
that constrain the LLM's responses (Grade, RouteIdentifier, VerificationResult).

Constraining LLM output to a typed schema is what makes it *testable*, so
these models are the foundation everything else asserts against.
"""

import pytest
from pydantic import ValidationError

from src.models.query_request import QueryRequest
from src.models.grade import Grade
from src.models.route_identifier import RouteIdentifier
from src.models.verification_result import VerificationResult


class TestQueryRequest:
    def test_valid_request(self):
        req = QueryRequest(query="What is the pet policy?", session_id="abc123")
        assert req.query == "What is the pet policy?"
        assert req.session_id == "abc123"

    def test_query_is_required(self):
        with pytest.raises(ValidationError):
            QueryRequest(session_id="abc123")

    def test_session_id_is_required(self):
        with pytest.raises(ValidationError):
            QueryRequest(query="hello")


class TestGrade:
    def test_valid_scores(self):
        assert Grade(binary_score="yes").binary_score == "yes"
        assert Grade(binary_score="no").binary_score == "no"

    def test_binary_score_required(self):
        with pytest.raises(ValidationError):
            Grade()


class TestRouteIdentifier:
    @pytest.mark.parametrize("route", ["index", "general", "web"])
    def test_valid_routes(self, route):
        assert RouteIdentifier(route=route).route == route

    def test_route_required(self):
        with pytest.raises(ValidationError):
            RouteIdentifier()


class TestVerificationResult:
    def test_valid_faithful(self):
        result = VerificationResult(faithful=True, explanation="Supported by context.")
        assert result.faithful is True
        assert result.explanation

    def test_faithful_must_be_bool(self):
        # A non-coercible value for a bool field should fail validation.
        with pytest.raises(ValidationError):
            VerificationResult(faithful="definitely", explanation="x")

    def test_fields_required(self):
        with pytest.raises(ValidationError):
            VerificationResult(faithful=True)
