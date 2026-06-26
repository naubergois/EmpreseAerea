"""Controller de QA — expõe os resultados dos testes BDD."""
from fastapi import APIRouter, HTTPException

from . import service

router = APIRouter(prefix="/api/qa", tags=["QA / Testes BDD"])


@router.get("/bdd")
def listar_testes_bdd(run: bool = False):
    """Lista todos os testes BDD com o motivo e o status (passou/falhou/pendente).

    - `run=false` (padrão): retorna o último resultado em cache, executando uma
      vez se ainda não houver cache.
    - `run=true`: força uma nova execução da suíte behave.
    """
    try:
        return service.get_bdd(force=run)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@router.post("/bdd/run")
def executar_testes_bdd():
    """Executa a suíte BDD novamente e retorna o relatório atualizado."""
    try:
        return service.run_bdd()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
