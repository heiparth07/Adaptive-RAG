"""
API / endpoint tests.

These exercise the *real* FastAPI route handlers in src/api/routes.py
(including their input-validation logic) through a TestClient, while the
external collaborators they call — the compiled graph, Mongo chat history,
and document ingestion — are mocked in conftest.py.

Covers: health/root, the RAG query contract and its validation rules, the
session-clear endpoint, and the document-upload endpoint.
"""


class TestHealthAndRoot:
    def test_health_check(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_root(self, client):
        resp = client.get("/")
        assert resp.status_code == 200
        assert "message" in resp.json()


class TestRagQuery:
    def test_valid_query_returns_answer(self, client):
        resp = client.post(
            "/rag/query",
            json={"query": "What is the pet policy?", "session_id": "s1"},
        )
        assert resp.status_code == 200
        body = resp.json()
        assert "result" in body
        # The mocked graph returns a canned AIMessage.
        assert body["result"]["content"] == "mocked answer"

    def test_empty_query_rejected(self, client):
        resp = client.post("/rag/query", json={"query": "", "session_id": "s1"})
        assert resp.status_code == 400
        assert "empty" in resp.json()["detail"].lower()

    def test_whitespace_only_query_rejected(self, client):
        resp = client.post("/rag/query", json={"query": "   ", "session_id": "s1"})
        assert resp.status_code == 400
        assert "empty" in resp.json()["detail"].lower()

    def test_too_long_query_rejected(self, client):
        resp = client.post(
            "/rag/query",
            json={"query": "a" * 2001, "session_id": "s1"},
        )
        assert resp.status_code == 400
        assert "too long" in resp.json()["detail"].lower()

    def test_query_at_max_length_allowed(self, client):
        resp = client.post(
            "/rag/query",
            json={"query": "a" * 2000, "session_id": "s1"},
        )
        assert resp.status_code == 200

    def test_missing_session_id_is_unprocessable(self, client):
        # Pydantic request-model validation -> 422 before our handler runs.
        resp = client.post("/rag/query", json={"query": "hello"})
        assert resp.status_code == 422


class TestClearSession:
    def test_valid_session_cleared(self, client):
        resp = client.delete("/rag/session/abc123")
        assert resp.status_code == 200
        assert resp.json()["status"] == "success"
        assert "abc123" in resp.json()["message"]

    def test_whitespace_session_rejected(self, client):
        # "%20" decodes to a single space -> stripped empty -> 400.
        resp = client.delete("/rag/session/%20")
        assert resp.status_code == 400
        assert "empty" in resp.json()["detail"].lower()


class TestDocumentUpload:
    def test_valid_upload(self, client):
        resp = client.post(
            "/rag/documents/upload",
            files={"file": ("doc.txt", b"hello world", "text/plain")},
            headers={"X-Description": "A community rules document"},
        )
        assert resp.status_code == 200
        assert resp.json()["status"] is True

    def test_missing_description_header_is_unprocessable(self, client):
        resp = client.post(
            "/rag/documents/upload",
            files={"file": ("doc.txt", b"hello world", "text/plain")},
        )
        assert resp.status_code == 422
