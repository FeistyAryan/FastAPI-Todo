from uuid import UUID
from contextvars import ContextVar

request_id_var: ContextVar[UUID | None] = ContextVar("request_id", default=None)