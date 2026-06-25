"""Controller de precificação."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from shared.exceptions import BusinessError

from .schemas import CupomValidacaoRequest, CupomValidacaoResponse, PrecoRequest, PrecoResponse
from .service import PrecificacaoService

router = APIRouter(prefix="/api/preco", tags=["Precificação"])


@router.post("/calcular", response_model=PrecoResponse)
def calcular_preco(request: PrecoRequest, db: Session = Depends(get_db)):
    return PrecificacaoService(db).calcular(request)


@router.post("/cupom/validar", response_model=CupomValidacaoResponse)
def validar_cupom(request: CupomValidacaoRequest, db: Session = Depends(get_db)):
    return PrecificacaoService(db).validar_cupom(request)


@router.get("/cotacao/{cotacao_id}", response_model=PrecoResponse)
def obter_cotacao(cotacao_id: str, db: Session = Depends(get_db)):
    try:
        result = PrecificacaoService(db).obter_cotacao(cotacao_id)
    except BusinessError as e:
        raise HTTPException(status_code=422, detail={"code": e.code, "message": str(e)})
    if not result:
        raise HTTPException(status_code=404, detail="Cotação não encontrada")
    return result
