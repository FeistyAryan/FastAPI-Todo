import time
import uuid
import structlog
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from fastapi import Response

from app.core.context import request_id_var

log = structlog.get_logger()

class CorrelationIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get("X-Request-ID")
        if not request_id:
            request_id = str(uuid.uuid4())
        
        request_id_var.set(uuid.UUID(request_id))

        start_time = time.time()
        response = await call_next(request)
        process_time = (time.time() - start_time) * 1000
        log.info(
            "request_processed",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            process_time_ms=round(process_time, 2),
            request_id=str(request_id_var.get())
        )
        
        response.headers["X-Request-ID"] = str(request_id_var.get())
        
        return response
    