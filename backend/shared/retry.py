"""Retry com backoff exponencial."""
import time
from collections.abc import Callable
from typing import TypeVar

from config import get_settings

T = TypeVar("T")


def retry_with_backoff(
    fn: Callable[[], T],
    max_attempts: int | None = None,
    base_delay: float = 0.1,
) -> T:
    """Executa função com retry exponencial."""
    attempts = max_attempts or get_settings().max_retry_attempts
    last_error: Exception | None = None
    for i in range(attempts):
        try:
            return fn()
        except Exception as exc:
            last_error = exc
            if i < attempts - 1:
                time.sleep(base_delay * (2**i))
    raise last_error  # type: ignore[misc]
