"""Singleton de Event Bus para comunicação entre agentes."""
from collections import defaultdict
from typing import Any, Callable


class EventBus:
    """Bus de eventos publish/subscribe."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._subscribers: dict[str, list[Callable]] = defaultdict(list)
            cls._instance._history: list[dict[str, Any]] = []
        return cls._instance

    def subscribe(self, event_type: str, handler: Callable) -> None:
        self._subscribers[event_type].append(handler)

    def publish(self, event_type: str, data: dict | None = None) -> None:
        payload = data or {}
        self._history.append({"type": event_type, "data": payload})
        for handler in self._subscribers[event_type]:
            handler(payload)

    def clear(self) -> None:
        self._subscribers.clear()
        self._history.clear()

    def get_history(self) -> list[dict[str, Any]]:
        return list(self._history)


event_bus = EventBus()


class Events:
    SEARCH_COMPLETED = "search.flights.completed"
    SEARCH_NO_RESULTS = "search.no_results"
    PRICING_READY = "pricing.quote.ready"
    RESERVA_CRIADA = "reservation.confirmed"
    RESERVA_CANCELADA = "reservation.cancelled"
    RESERVA_EXPIRADA = "reservation.expired"
    PAGAMENTO_CONFIRMADO = "payment.approved"
    PAGAMENTO_RECUSADO = "payment.declined"
    BILHETE_EMITIDO = "ticket.issued"
    BILHETE_FALHA = "ticket.issue.failed"
    MILHAS_ACUMULADAS = "loyalty.credited"
    NOTIFICACAO_ENVIADA = "notification.delivered"
    CAMPANHA_ENVIADA = "marketing.campaign.sent"
    CARRINHO_ABANDONADO = "cart.abandoned"
    REEMBOLSO_PROCESSADO = "refund.processed"
