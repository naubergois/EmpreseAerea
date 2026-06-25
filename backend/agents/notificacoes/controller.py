"""Controller de notificações."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db

from .schemas import NotificacaoRequest, NotificacaoResponse, PreferenciasRequest
from .service import NotificacaoService

router = APIRouter(prefix="/api/notificacao", tags=["Notificações"])


@router.post("/enviar", response_model=NotificacaoResponse, status_code=201)
def enviar(request: NotificacaoRequest, db: Session = Depends(get_db)):
    return NotificacaoService(db).enviar(request)


@router.get("/{notif_id}/status", response_model=NotificacaoResponse)
def status(notif_id: int, db: Session = Depends(get_db)):
    try:
        return NotificacaoService(db).status(notif_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/preferencias")
def preferencias(request: PreferenciasRequest, db: Session = Depends(get_db)):
    return NotificacaoService(db).atualizar_preferencias(request)
