"""Service de atendimento com LLM."""
import logging

from sqlalchemy.orm import Session

from shared.datetime_utils import utc_now

from .context_builder import extrair_pnr, montar_contexto
from .faq_engine import responder_faq
from .llm_client import llm_client
from .models import Atendimento
from .schemas import ChatRequest, ChatResponse, EscalarRequest
from .sentiment_analyzer import analisar

logger = logging.getLogger(__name__)


class AtendimentoService:
    def __init__(self, db: Session):
        self.db = db

    def _protocolo(self) -> str:
        return f"ATC-{utc_now().strftime('%Y%m%d')}-{self.db.query(Atendimento).count() + 1:03d}"

    async def _gerar_resposta(self, req: ChatRequest) -> tuple[str, bool]:
        pnr = extrair_pnr(req.mensagem, req.pnr)
        contexto = montar_contexto(self.db, pnr)

        if llm_client.enabled:
            try:
                resposta = await llm_client.chat(req.mensagem, contexto)
                escalado = "[ESCALAR]" in resposta
                resposta = resposta.replace("[ESCALAR]", "").strip()
                return resposta, escalado
            except Exception as exc:
                logger.warning("LLM indisponível, usando FAQ: %s", exc)

        faq = responder_faq(req.mensagem)
        if faq:
            return faq, False
        if contexto:
            return f"Encontrei sua reserva:\n{contexto}", False
        return (
            "Olá! Sou o assistente SkyAgent. Posso ajudar com reservas, bagagem, "
            "cancelamento, check-in e milhas. Informe seu PNR (6 caracteres) se quiser "
            "consultar uma reserva.",
            False,
        )

    async def chat(self, req: ChatRequest) -> ChatResponse:
        sentimento, urgente = analisar(req.mensagem)
        resposta, escalado_llm = await self._gerar_resposta(req)
        escalado = escalado_llm or (sentimento == "negativo" and urgente)

        atend = Atendimento(
            protocolo=self._protocolo(),
            canal=req.canal,
            mensagem=req.mensagem,
            resposta=resposta,
            sentimento=sentimento,
            status="escalado" if escalado else "aberto",
            idioma=req.idioma or "pt",
        )
        self.db.add(atend)
        self.db.commit()

        if escalado:
            resposta += "\n\nUm atendente humano dará continuidade em breve."

        return ChatResponse(
            protocolo=atend.protocolo,
            resposta=resposta,
            sentimento=sentimento,
            escalado=escalado,
        )

    def escalar(self, req: EscalarRequest) -> dict:
        atend = self.db.query(Atendimento).filter(Atendimento.protocolo == req.protocolo).first()
        if atend:
            atend.status = "escalado"
            self.db.commit()
        return {"protocolo": req.protocolo, "status": "escalado", "motivo": req.motivo}

    def historico(self, protocolo: str) -> dict:
        atend = self.db.query(Atendimento).filter(Atendimento.protocolo == protocolo).first()
        if not atend:
            raise ValueError("Protocolo não encontrado")
        return {
            "protocolo": atend.protocolo,
            "mensagem": atend.mensagem,
            "resposta": atend.resposta,
            "status": atend.status,
            "sentimento": atend.sentimento,
        }
