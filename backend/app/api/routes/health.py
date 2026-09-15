"""System Health Check Endpoint."""

from fastapi import APIRouter
from app.schemas.api import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def get_health():
    """Returns service health status without disclosing internal environment data."""
    return HealthResponse(status="ok", service="MailRakhwala API")