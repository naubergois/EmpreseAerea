"""Controller do orquestrador."""
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from .schemas import PipelineStartRequest, PipelineStatusResponse
from .service import OrquestradorService

router = APIRouter(prefix="/api/pipeline", tags=["Orquestrador"])


@router.get("/health")
def health(db: Session = Depends(get_db)):
    return OrquestradorService(db).health()


@router.post("/start", response_model=PipelineStatusResponse)
def iniciar_pipeline(request: PipelineStartRequest, db: Session = Depends(get_db)):
    try:
        return OrquestradorService(db).iniciar_pipeline(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{session_id}/status", response_model=PipelineStatusResponse)
def status_pipeline(session_id: str, db: Session = Depends(get_db)):
    try:
        return OrquestradorService(db).status(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/{session_id}/rollback")
def rollback(session_id: str, db: Session = Depends(get_db)):
    try:
        return OrquestradorService(db).rollback(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/classificar")
def classificar_intencao(mensagem: str, db: Session = Depends(get_db)):
    return {"intencao": OrquestradorService(db).classificar_intencao(mensagem)}
