from fastapi import APIRouter

from app.core.response import ok

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health():
    return ok({"status": "ok"})