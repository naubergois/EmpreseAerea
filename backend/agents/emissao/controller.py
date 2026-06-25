"""Controller de emissão."""
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from database import get_db
from shared.exceptions import BusinessError, NotFoundError

from .schemas import BilheteResponse, BoardingPassResponse, EmitirRequest
from .service import EmissaoService

router = APIRouter(prefix="/api/bilhete", tags=["Emissão"])


@router.post("/emitir", response_model=BilheteResponse, status_code=201)
def emitir(request: EmitirRequest, db: Session = Depends(get_db)):
    try:
        return EmissaoService(db).emitir(request)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{numero}", response_model=BilheteResponse)
def buscar(numero: str, db: Session = Depends(get_db)):
    try:
        return EmissaoService(db).buscar(numero)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/{numero}/pdf")
def pdf(numero: str, db: Session = Depends(get_db)):
    bp = EmissaoService(db).boarding_pass(numero)
    return JSONResponse({"boarding_pass": bp.model_dump(), "formato": "pdf"})


@router.post("/{numero}/void")
def void_bilhete(numero: str, db: Session = Depends(get_db)):
    try:
        return EmissaoService(db).void(numero)
    except (NotFoundError, BusinessError) as e:
        code = getattr(e, "code", "erro")
        raise HTTPException(status_code=422, detail={"code": code, "message": str(e)})


@router.post("/{numero}/reemitir", response_model=BilheteResponse)
def reemitir(numero: str, db: Session = Depends(get_db)):
    try:
        return EmissaoService(db).reemitir(numero)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
