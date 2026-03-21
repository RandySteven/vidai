from __future__ import annotations

from typing import Any


class Error(Exception):
    """Base application error."""

    pass


class AppError(Error):
    """Structured error for use cases: map to HTTP or wrap in ``Err``."""

    def __init__(
        self,
        message: str,
        *,
        code: str = "app_error",
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.status_code = status_code
        self.details = details or {}


class InvalidRequestError(AppError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, code="invalid_request", status_code=400, **kwargs)


class InvalidResponseError(AppError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, code="invalid_response", status_code=502, **kwargs)


class InvalidAPIKeyError(AppError):
    def __init__(self, message: str = "Invalid API key", **kwargs: Any) -> None:
        super().__init__(message, code="invalid_api_key", status_code=401, **kwargs)


class InvalidAPIResponseError(AppError):
    def __init__(self, message: str, **kwargs: Any) -> None:
        super().__init__(message, code="invalid_api_response", status_code=502, **kwargs)
