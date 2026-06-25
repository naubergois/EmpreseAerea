"""Implementação de circuit breaker por agente."""
import time
from enum import Enum

from config import get_settings


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit breaker simples por nome de serviço."""

    def __init__(self, name: str):
        self.name = name
        self.state = CircuitState.CLOSED
        self.failures = 0
        self.last_failure = 0.0
        self.threshold = get_settings().circuit_breaker_threshold

    def record_success(self) -> None:
        self.failures = 0
        self.state = CircuitState.CLOSED

    def record_failure(self) -> None:
        self.failures += 1
        self.last_failure = time.time()
        if self.failures >= self.threshold:
            self.state = CircuitState.OPEN

    def allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure > 30:
                self.state = CircuitState.HALF_OPEN
                return True
            return False
        return True


_breakers: dict[str, CircuitBreaker] = {}


def get_circuit_breaker(name: str) -> CircuitBreaker:
    if name not in _breakers:
        _breakers[name] = CircuitBreaker(name)
    return _breakers[name]
