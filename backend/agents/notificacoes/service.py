"""Service de notificações."""
from sqlalchemy.orm import Session

from event_bus import Events, event_bus

from .models import Notificacao, StatusNotificacao
from .schemas import NotificacaoRequest, NotificacaoResponse, PreferenciasRequest

TEMPLATES = {
    "confirmacao_compra": "Sua compra foi confirmada! PNR: {pnr}, Bilhete: {bilhete}",
    "pagamento_aprovado": "Pagamento aprovado para PNR {pnr}",
    "reserva_cancelada": "Sua reserva {pnr} foi cancelada",
    "alerta_voo": "Alerta: seu voo {voo} teve alteração",
}


class NotificacaoService:
    _preferencias: dict[str, dict] = {}

    def __init__(self, db: Session):
        self.db = db

    def enviar(self, req: NotificacaoRequest) -> NotificacaoResponse:
        template = TEMPLATES.get(req.tipo, "Notificação SkyAgent: {tipo}")
        conteudo = template.format(tipo=req.tipo, **req.dados)
        notif = Notificacao(
            tipo=req.tipo, canal=req.canal, destinatario=req.destinatario,
            conteudo=conteudo, status=StatusNotificacao.ENTREGUE,
        )
        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        event_bus.publish(Events.NOTIFICACAO_ENVIADA, {"id": notif.id, "tipo": req.tipo})
        return NotificacaoResponse(id=notif.id, tipo=req.tipo, canal=req.canal, status="entregue")

    def status(self, notif_id: int) -> NotificacaoResponse:
        n = self.db.query(Notificacao).filter(Notificacao.id == notif_id).first()
        if not n:
            raise ValueError("Notificação não encontrada")
        return NotificacaoResponse(id=n.id, tipo=n.tipo, canal=n.canal, status=n.status.value)

    def atualizar_preferencias(self, req: PreferenciasRequest) -> dict:
        self._preferencias[req.cliente_id] = req.model_dump()
        return {"cliente_id": req.cliente_id, "atualizado": True}
