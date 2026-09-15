"""Tests verifying Step 5 FastAPI Backend Core."""

import io
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.job_store import job_store
from app.core.config import settings

client = TestClient(app)


@pytest.fixture(autouse=True)
def clean_job_store():
    job_store.clear()
    yield
    job_store.clear()


def test_health_check_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "MailRakhwala API"


def test_upload_no_file():
    response = client.post("/analysis/upload")
    assert response.status_code == 422


def test_upload_empty_file():
    payload = io.BytesIO(b"")
    response = client.post(
        "/analysis/upload",
        files={"file": ("empty.pcap", payload, "application/vnd.tcpdump.pcap")}
    )
    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_upload_unsupported_extension():
    payload = io.BytesIO(b"fake binary payload")
    response = client.post(
        "/analysis/upload",
        files={"file": ("malicious.exe", payload, "application/octet-stream")}
    )
    assert response.status_code == 400
    assert "unsupported" in response.json()["detail"].lower()


def test_upload_valid_pcap():
    payload = io.BytesIO(b"\xd4\xc3\xb2\xa1test-pcap-content")
    response = client.post(
        "/analysis/upload",
        files={"file": ("session.pcap", payload, "application/vnd.tcpdump.pcap")}
    )
    assert response.status_code == 202
    data = response.json()
    assert "analysis_id" in data
    assert data["status"] == "queued"
    assert data["filename"] == "session.pcap"


def test_upload_valid_pcapng():
    payload = io.BytesIO(b"\x0a\x0d\x0d\x0atest-pcapng-content")
    response = client.post(
        "/analysis/upload",
        files={"file": ("session.pcapng", payload, "application/octet-stream")}
    )
    assert response.status_code == 202
    data = response.json()
    assert data["status"] == "queued"
    assert data["filename"] == "session.pcapng"


def test_get_analysis_status_lifecycle():
    payload = io.BytesIO(b"\xd4\xc3\xb2\xa1test-content")
    upload_resp = client.post(
        "/analysis/upload",
        files={"file": ("capture.pcap", payload, "application/vnd.tcpdump.pcap")}
    )
    analysis_id = upload_resp.json()["analysis_id"]

    get_resp = client.get(f"/analysis/{analysis_id}")
    assert get_resp.status_code == 200
    job_data = get_resp.json()
    assert job_data["analysis_id"] == analysis_id
    assert job_data["status"] == "queued"
    assert job_data["filename"] == "capture.pcap"
    assert job_data["file_size_bytes"] > 0


def test_get_analysis_unknown_id():
    response = client.get("/analysis/non-existent-uuid-12345")
    assert response.status_code == 404


def test_upload_oversized_file(monkeypatch):
    monkeypatch.setattr(type(settings), "max_upload_bytes", property(lambda self: 10))

    oversized_data = io.BytesIO(b"A" * 50)
    response = client.post(
        "/analysis/upload",
        files={"file": ("large.pcap", oversized_data, "application/vnd.tcpdump.pcap")}
    )
    assert response.status_code == 413
    assert "exceeds" in response.json()["detail"].lower()


def test_path_traversal_filename_sanitization_and_containment():
    payload = io.BytesIO(b"\xd4\xc3\xb2\xa1data")
    traversal_filename = "../../../../../etc/shadow.pcap"
    
    response = client.post(
        "/analysis/upload",
        files={"file": (traversal_filename, payload, "application/vnd.tcpdump.pcap")}
    )
    assert response.status_code == 202
    data = response.json()
    
    assert data["filename"] == "shadow.pcap"
    analysis_id = data["analysis_id"]

    job = job_store.get_job(analysis_id)
    assert job is not None
    
    stored_path = Path(job.storage_path).resolve()
    upload_root = settings.UPLOAD_DIR.resolve()

    assert upload_root in stored_path.parents or stored_path.parent == upload_root
    assert stored_path.name == f"{analysis_id}.pcap"
    assert stored_path.exists()

    stored_path.unlink(missing_ok=True)