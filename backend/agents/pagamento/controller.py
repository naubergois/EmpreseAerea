"""Controller de pagamento."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from shared.exceptions import BusinessError

from .schemas import (
    PagamentoBoletoRequest,
    PagamentoCartaoRequest,
    PagamentoPixRequest,
    PagamentoResponse,
    PagamentoSplitRequest,
    ReembolsoRequest,
)
from .service import PagamentoService

router = APIRouter(prefix="/api/pagamento", tags=["Pagamento"])


def _handle(exc: BusinessError):
    raise HTTPException(status_code=422, detail={"code": exc.code, "message": str(exc)})


@router.post("/cartao", response_model=PagamentoResponse)
def pagar_cartao(request: PagamentoCartaoRequest, db: Session = Depends(get_db)):
    try:
        return PagamentoService(db).pagar_cartao(request)
    except BusinessError as e:
        _handle(e)


@router.post("/pix", response_model=PagamentoResponse)
def gerar_pix(request: PagamentoPixRequest, db: Session = Depends(get_db)):
    return PagamentoService(db).gerar_pix(request)


@router.post("/webhook/pix", response_model=PagamentoResponse)
def webhook_pix(txn_id: str, valor: float, db: Session = Depends(get_db)):
    try:
        return PagamentoService(db).webhook_pix(txn_id, valor)
    except BusinessError as e:
        _handle(e)


@router.post("/boleto", response_model=PagamentoResponse)
def gerar_boleto(request: PagamentoBoletoRequest, db: Session = Depends(get_db)):
    return PagamentoService(db).gerar_boleto(request)


@router.get("/{txn_id}/status", response_model=PagamentoResponse)
def status_pagamento(txn_id: str, db: Session = Depends(get_db)):
    try:
        return PagamentoService(db).status(txn_id)
    except BusinessError as e:
        _handle(e)


@router.post("/{txn_id}/reembolso")
def reembolso(txn_id: str, request: ReembolsoRequest, db: Session = Depends(get_db)):
    try:
        return PagamentoService(db).reembolsar(txn_id, request)
    except BusinessError as e:
        _handle(e)


@router.post("/split", response_model=PagamentoResponse)
def pagar_split(request: PagamentoSplitRequest, db: Session = Depends(get_db)):
    return PagamentoService(db).pagar_split(request)
