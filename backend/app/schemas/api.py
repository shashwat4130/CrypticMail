"""
CrypticMail API Request & Response Schemas
HTTP contracts for health and analysis ingestion.
"""

from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    QUEUED = "queued"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class HealthResponse(BaseModel):
    status: str = Field(default="ok")
    service: str = Field(default="CrypticMail API")


class AnalysisUploadResponse(BaseModel):
    analysis_id: str = Field(..., description="Unique UUID for tracking the analysis job")
    status: JobStatus = Field(default=JobStatus.QUEUED)
    filename: str = Field(..., description="Sanitized original filename")
    message: str = Field(default="Capture uploaded successfully and queued for analysis")


class AnalysisJobResponse(BaseModel):
    analysis_id: str
    status: JobStatus
    filename: str
    file_size_bytes: int
    created_at: datetime
    updated_at: datetime
    message: Optional[str] = None