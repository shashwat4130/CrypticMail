"""
MailRakhwala Application Configuration
"""

from pathlib import Path
from typing import List
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    APP_ENV: str = Field(default="development", description="Application runtime environment")
    MAX_PCAP_SIZE_MB: int = Field(default=100, ge=1, le=1000, description="Max upload size limit in MB")

    # Upload storage directory
    UPLOAD_DIR: Path = Field(
        default=Path(__file__).resolve().parent.parent.parent / "data" / "uploads"
    )

    # Allowed frontend development origins
    CORS_ORIGINS: List[str] = Field(
        default=["http://localhost:5173", "http://127.0.0.1:5173"]
    )

    @property
    def max_upload_bytes(self) -> int:
        return self.MAX_PCAP_SIZE_MB * 1024 * 1024

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Export singleton instance
settings = Settings()
settings.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)