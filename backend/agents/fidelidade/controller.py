"""Controller de fidelidade."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from shared.exceptions import BusinessError

from .schemas import AcumularRequest, ExtratoItem, MilhasResponse, NivelResponse, ResgatarRequest
from .service import FidelidadeService

router = APIRouter(prefix="/api/fidelidade", tags=["Fidelidade"])


@router.get("/{cliente_id}/saldo", response_model=MilhasResponse)
def saldo(cliente_id: str, db: Session = Depends(get_db)):
    return FidelidadeService(db).saldo(cliente_id)


@router.post("/acumular", response_model=MilhasResponse)
def acumular(request: AcumularRequest, db: Session = Depends(get_db)):
    return FidelidadeService(db).acumular(request)


@router.post("/resgatar", response_model=MilhasResponse)
def resgatar(request: ResgatarRequest, db: Session = Depends(get_db)):
    try:
        return FidelidadeService(db).resgatar(request)
    except BusinessError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": str(e)})


@router.get("/{cliente_id}/extrato", response_model=list[ExtratoItem])
def extrato(cliente_id: str, db: Session = Depends(get_db)):
    return FidelidadeService(db).extrato(cliente_id)


@router.get("/{cliente_id}/nivel", response_model=NivelResponse)
def nivel(cliente_id: str, db: Session = Depends(get_db)):
    return FidelidadeService(db).nivel(cliente_id)
