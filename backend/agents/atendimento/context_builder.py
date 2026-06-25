"""Monta contexto de atendimento a partir de PNR e histórico."""
import re

from sqlalchemy.orm import Session

PNR_PATTERN = re.compile(r"\b[A-Z0-9]{6}\b", re.IGNORECASE)


def extrair_pnr(texto: str, pnr_informado: str | None = None) -> str | None:
    if pnr_informado:
        return pnr_informado.upper()
    match = PNR_PATTERN.search(texto.upper())
    return match.group(0).upper() if match else None


def montar_contexto(db: Session, pnr: str | None) -> str:
    if not pnr:
        return ""

    from agents.reserva.models import Reserva

    reserva = db.query(Reserva).filter(Reserva.pnr == pnr.upper()).first()
    if not reserva:
        return f"PNR {pnr}: não encontrado no sistema."

    pax = ", ".join(f"{p.nome} {p.sobrenome}" for p in reserva.passageiros)
    return (
        f"PNR: {reserva.pnr}\n"
        f"Status: {reserva.status.value}\n"
        f"Rota: {reserva.origem} → {reserva.destino}\n"
        f"Voo: {reserva.voo_ida}\n"
        f"Valor: R$ {reserva.valor_total:.2f}\n"
        f"Passageiros: {pax or 'N/A'}\n"
        f"Expira em: {reserva.expira_em.isoformat()}"
    )
