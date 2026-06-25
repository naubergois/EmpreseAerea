"""Service do orquestrador."""
import json
import uuid
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from config import get_settings
from event_bus import Events, event_bus

from agents.busca_voos.schemas import BuscaRequest
from agents.busca_voos.service import BuscaService
from agents.emissao.schemas import EmitirRequest
from agents.emissao.service import EmissaoService
from agents.fidelidade.schemas import AcumularRequest
from agents.fidelidade.service import FidelidadeService
from agents.notificacoes.schemas import NotificacaoRequest
from agents.notificacoes.service import NotificacaoService
from agents.pagamento.schemas import PagamentoCartaoRequest, PagamentoPixRequest
from agents.pagamento.service import PagamentoService
from agents.precificacao.schemas import PrecoRequest
from agents.precificacao.service import PrecificacaoService
from agents.reserva.schemas import PassageiroInput, ReservaRequest
from agents.reserva.service import ReservaService

from .models import EtapaAuditoria, PipelineStatus, SessaoPipeline
from .saga import SagaOrchestrator
from .schemas import PipelineStartRequest, PipelineStatusResponse, EtapaStatus


class OrquestradorService:
    ETAPAS = [
        ("Busca", "BUS"), ("Precificação", "PRE"), ("Reserva", "RES"),
        ("Pagamento", "PAG"), ("Emissão", "EMI"), ("Milhas", "FID"), ("Notificação", "NOT"),
    ]

    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()

    def iniciar_pipeline(self, req: PipelineStartRequest) -> PipelineStatusResponse:
        session_id = f"SES-{uuid.uuid4().hex[:8].upper()}"
        trace_id = f"TRC-{uuid.uuid4().hex[:12].upper()}"
        expira = datetime.utcnow() + timedelta(minutes=self.settings.session_timeout_minutes)

        sessao = SessaoPipeline(
            id=session_id, trace_id=trace_id, status=PipelineStatus.EM_PROGRESSO,
            estado_json="{}", nivel_fidelidade=req.nivel_fidelidade, expira_em=expira,
        )
        self.db.add(sessao)
        self.db.commit()

        saga = SagaOrchestrator(self.db)
        etapas: list[EtapaStatus] = []
        estado: dict = {}
        resultado: dict = {}

        try:
            busca = BuscaService(self.db).buscar(BuscaRequest(
                origem=req.origem, destino=req.destino, data_ida=req.data_ida,
            ))
            etapas.append(self._registrar_etapa(session_id, "Busca", "BUS", "Sucesso"))
            estado["voos"] = len(busca.voos)

            voo_id = req.voo_id or (busca.voos[0].id if busca.voos else "LA3421")
            preco_base = req.preco_base or (busca.voos[0].preco if busca.voos else 450)
            preco = PrecificacaoService(self.db).calcular(PrecoRequest(
                voo_id=voo_id, preco_base=preco_base, nivel_fidelidade=req.nivel_fidelidade,
            ))
            etapas.append(self._registrar_etapa(session_id, "Precificação", "PRE", "Sucesso"))
            estado["cotacao_id"] = preco.cotacao_id
            estado["valor"] = preco.valor_total

            passageiros = req.passageiros or [{
                "nome": "João", "sobrenome": "Silva",
                "cpf": "529.982.247-25",
                "data_nascimento": "1990-01-15T00:00:00",
                "tipo": "ADT",
            }]
            reserva_req = ReservaRequest(
                voo_ida=voo_id, data_ida=req.data_ida, origem=req.origem,
                destino=req.destino, valor_total=preco.valor_total,
                passageiros=[PassageiroInput(**p) for p in passageiros],
            )
            reserva = ReservaService(self.db).criar_reserva(reserva_req)
            saga.registrar(lambda pnr=reserva.pnr: ReservaService(self.db).cancelar(pnr))
            etapas.append(self._registrar_etapa(session_id, "Reserva", "RES", "Sucesso"))
            estado["pnr"] = reserva.pnr

            if req.metodo_pagamento == "pix":
                pag = PagamentoService(self.db).gerar_pix(
                    PagamentoPixRequest(pnr=reserva.pnr, valor=preco.valor_total)
                )
                PagamentoService(self.db).webhook_pix(pag.id, preco.valor_total)
            else:
                cartao = req.cartao or {
                    "numero_cartao": "4111111111111111", "nome_titular": "JOAO",
                    "validade": "12/28", "cvv": "123",
                }
                pag = PagamentoService(self.db).pagar_cartao(
                    PagamentoCartaoRequest(pnr=reserva.pnr, valor=preco.valor_total, **cartao)
                )
            etapas.append(self._registrar_etapa(session_id, "Pagamento", "PAG", "Sucesso"))
            estado["pagamento_id"] = pag.id

            bilhete = EmissaoService(self.db).emitir(
                EmitirRequest(pnr=reserva.pnr, pagamento_id=pag.id)
            )
            etapas.append(self._registrar_etapa(session_id, "Emissão", "EMI", "Sucesso"))
            estado["bilhete"] = bilhete.numero

            FidelidadeService(self.db).acumular(AcumularRequest(
                cliente_id=req.cliente_id, pnr=reserva.pnr, valor=preco.valor_total,
                nivel=req.nivel_fidelidade or "Bronze",
            ))
            etapas.append(self._registrar_etapa(session_id, "Milhas", "FID", "Sucesso"))

            NotificacaoService(self.db).enviar(NotificacaoRequest(
                tipo="confirmacao_compra", destinatario="cliente@email.com",
                dados={"pnr": reserva.pnr, "bilhete": bilhete.numero},
            ))
            etapas.append(self._registrar_etapa(session_id, "Notificação", "NOT", "Sucesso"))

            sessao.status = PipelineStatus.SUCESSO
            resultado = {"pnr": reserva.pnr, "bilhete": bilhete.numero, "valor": preco.valor_total}

        except Exception as exc:
            saga.rollback(estado.get("pnr"), str(exc))
            sessao.status = PipelineStatus.ROLLBACK
            etapas.append(EtapaStatus(etapa="Rollback", agente="ORC", status="Executado"))
            raise

        finally:
            sessao.estado_json = json.dumps(estado)
            sessao.atualizado_em = datetime.utcnow()
            self.db.commit()

        return PipelineStatusResponse(
            session_id=session_id, trace_id=trace_id, status="sucesso",
            etapas=etapas, resultado=resultado,
        )

    def status(self, session_id: str) -> PipelineStatusResponse:
        sessao = self.db.query(SessaoPipeline).filter(SessaoPipeline.id == session_id).first()
        if not sessao:
            raise ValueError("Sessão não encontrada")
        etapas_db = self.db.query(EtapaAuditoria).filter(EtapaAuditoria.sessao_id == session_id).all()
        etapas = [EtapaStatus(etapa=e.etapa, agente=e.agente, status=e.status) for e in etapas_db]
        return PipelineStatusResponse(
            session_id=sessao.id, trace_id=sessao.trace_id,
            status=sessao.status.value, etapas=etapas,
            resultado=json.loads(sessao.estado_json) if sessao.estado_json else None,
        )

    def rollback(self, session_id: str) -> dict:
        sessao = self.db.query(SessaoPipeline).filter(SessaoPipeline.id == session_id).first()
        if not sessao:
            raise ValueError("Sessão não encontrada")
        estado = json.loads(sessao.estado_json or "{}")
        saga = SagaOrchestrator(self.db)
        result = saga.rollback(estado.get("pnr"), "rollback_manual")
        sessao.status = PipelineStatus.ROLLBACK
        self.db.commit()
        return result

    def classificar_intencao(self, mensagem: str) -> str:
        msg = mensagem.lower()
        if "cancel" in msg:
            return "cancelamento"
        if "mudar" in msg or "alter" in msg:
            return "alteração_de_reserva"
        if "voo" in msg and "busc" in msg:
            return "busca"
        return "suporte"

    def health(self) -> dict:
        agentes = ["BUS", "PRE", "RES", "PAG", "EMI", "FID", "NOT", "MKT", "ATC", "ORC"]
        return {"agentes": {a: "healthy" for a in agentes}}

    def _registrar_etapa(self, sessao_id: str, etapa: str, agente: str, status: str) -> EtapaStatus:
        self.db.add(EtapaAuditoria(sessao_id=sessao_id, etapa=etapa, agente=agente, status=status))
        self.db.commit()
        return EtapaStatus(etapa=etapa, agente=agente, status=status)
