"""
CrypticMail Capture Ingestion & Analysis Routes
Handles secure bounded file upload and job state tracking.
"""

import uuid
from pathlib import Path
from typing import Optional
from fastapi import APIRouter, File, HTTPException, UploadFile, status

from app.core.config import settings
from app.schemas.api import AnalysisJobResponse, AnalysisUploadResponse, JobStatus
from app.services.job_store import job_store

router = APIRouter(prefix="/analysis", tags=["Analysis"])

ALLOWED_EXTENSIONS = {".pcap", ".pcapng"}


def sanitize_filename(filename: Optional[str]) -> str:
    """Strips directory traversal sequences and isolates the base filename."""
    if not filename:
        return "unnamed_capture.pcap"
    return Path(filename).name


@router.post(
    "/upload",
    response_model=AnalysisUploadResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Upload PCAP/PCAPNG capture for forensic assessment"
)
async def upload_capture(file: UploadFile = File(...)):
    original_name = file.filename or ""
    clean_name = sanitize_filename(original_name)
    suffix = Path(clean_name).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type '{suffix}'. Allowed formats: {sorted(list(ALLOWED_EXTENSIONS))}"
        )

    analysis_id = str(uuid.uuid4())
    safe_disk_filename = f"{analysis_id}{suffix}"
    destination = settings.UPLOAD_DIR / safe_disk_filename

    total_bytes = 0
    chunk_size = 1024 * 1024  # 1MB buffer

    try:
        with open(destination, "wb") as buffer:
            while chunk := await file.read(chunk_size):
                total_bytes += len(chunk)
                if total_bytes > settings.max_upload_bytes:
                    buffer.close()
                    destination.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Capture exceeds maximum allowed size of {settings.MAX_PCAP_SIZE_MB}MB"
                    )
                buffer.write(chunk)
    except HTTPException:
        raise
    except Exception as exc:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to persist uploaded capture safely."
        ) from exc

    if total_bytes == 0:
        destination.unlink(missing_ok=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded capture file is empty."
        )

    job_store.create_job(
        analysis_id=analysis_id,
        filename=clean_name,
        storage_path=str(destination),
        file_size_bytes=total_bytes
    )

    return AnalysisUploadResponse(
        analysis_id=analysis_id,
        status=JobStatus.QUEUED,
        filename=clean_name,
        message="Capture uploaded successfully and queued for analysis."
    )


@router.get(
    "/{analysis_id}",
    response_model=AnalysisJobResponse,
    summary="Query status of an analysis job"
)
async def get_analysis_job(analysis_id: str):
    job = job_store.get_job(analysis_id)
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis ID '{analysis_id}' not found."
        )
    return job.to_response()