""" """

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


async def http_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle HTTPException."""
    if isinstance(exc, HTTPException):
        return JSONResponse(
            headers=exc.headers,
            status_code=exc.status_code,
            content={"status": exc.status_code, "message": str(exc.detail)},
        )
    raise exc
