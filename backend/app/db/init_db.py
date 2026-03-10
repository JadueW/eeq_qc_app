from pathlib import Path

from app.core.config import settings
from app.core.database import engine
from app.db.models import Base


def init_db() -> None:
    for path in [
        settings.data_dir,
        settings.upload_dir,
        settings.bids_dir,
        settings.report_dir,
    ]:
        Path(path).mkdir(parents=True, exist_ok=True)

    Base.metadata.create_all(bind=engine)