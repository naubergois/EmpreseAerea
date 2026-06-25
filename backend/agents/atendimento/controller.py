"""Controller de atendimento."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from .schemas import ChatRequest, ChatResponse, EscalarRequest
from .service import AtendimentoService

router = APIRouter(prefix="/api/atendimento", tags=["Atendimento"])


@router.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    return AtendimentoService(db).chat(request)


@router.post("/escalar")
def escalar(request: EscalarRequest, db: Session = Depends(get_db)):
    return AtendimentoService(db).escalar(request)


@router.get("/{protocolo}")
def historico(protocolo: str, db: Session = Depends(get_db)):
    try:
        return AtendimentoService(db).historico(protocolo)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
