from typing import Any


def ok(data: Any = None, message: str = "") -> dict:
    return {"code": 0, "data": data, "message": message}


def fail(message: str = "error", code: int = 1, data: Any = None) -> dict:
    return {"code": code, "data": data, "message": message}