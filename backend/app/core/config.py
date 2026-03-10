from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "EEG QC"
    app_env: str = "dev"
    data_dir: Path = Path("backend/data")
    upload_dir: Path = Path("backend/data/uploads")
    bids_dir: Path = Path("backend/data/bids")
    report_dir: Path = Path("backend/data/reports")
    sqlite_path: Path = Path("backend/data/app.db")
    max_workers: int = 4
    cors_origins: list[str] = ["http://localhost:5173"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()