"""Controller de reserva."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from shared.exceptions import BusinessError, NotFoundError, ValidationError

from .schemas import AssentoRequest, PassageiroResponse, ReservaRequest, ReservaResponse
from .service import ReservaService

router = APIRouter(prefix="/api/reserva", tags=["Reserva"])


def _to_response(reserva) -> ReservaResponse:
    return ReservaResponse(
        pnr=reserva.pnr,
        status=reserva.status.value,
        voo_ida=reserva.voo_ida,
        origem=reserva.origem,
        destino=reserva.destino,
        valor_total=reserva.valor_total,
        expira_em=reserva.expira_em,
        passageiros=[
            PassageiroResponse(
                id=p.id, nome=p.nome, sobrenome=p.sobrenome, cpf=p.cpf,
                passaporte=p.passaporte, data_nascimento=p.data_nascimento,
                tipo=p.tipo, assento=p.assento, email=p.email, telefone=p.telefone,
            )
            for p in reserva.passageiros
        ],
    )


@router.post("/", response_model=ReservaResponse, status_code=201)
def criar_reserva(request: ReservaRequest, db: Session = Depends(get_db)):
    try:
        return ReservaService(db).criar_reserva(request)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except BusinessError as e:
        raise HTTPException(status_code=422, detail=f"{e.code}: {e}")


@router.get("/{pnr}", response_model=ReservaResponse)
def buscar_reserva(pnr: str, db: Session = Depends(get_db)):
    try:
        return _to_response(ReservaService(db).buscar(pnr))
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{pnr}", status_code=204)
def cancelar_reserva(pnr: str, db: Session = Depends(get_db)):
    try:
        ReservaService(db).cancelar(pnr)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{pnr}/assento")
def selecionar_assento(pnr: str, request: AssentoRequest, db: Session = Depends(get_db)):
    try:
        return ReservaService(db).selecionar_assento(pnr, request)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
