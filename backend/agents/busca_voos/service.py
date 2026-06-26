"""Service de busca de voos."""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from event_bus import Events, event_bus
from shared.circuit_breaker import get_circuit_breaker

from .gds_client import gerar_voos, resolver_aeroportos
from .repository import BuscaRepository
from .schemas import BuscaRequest, BuscaResponse, VooResponse


class BuscaService:
    def __init__(self, db: Session):
        self.repo = BuscaRepository(db)
        self.breaker = get_circuit_breaker("BUS")

    def buscar(self, req: BuscaRequest) -> BuscaResponse:
        if not self.breaker.allow_request():
            raise RuntimeError("Agente de Busca indisponível (circuit breaker aberto)")

        origens = resolver_aeroportos(req.origem)
        destinos = resolver_aeroportos(req.destino)
        chave = f"{origens}-{destinos}-{req.data_ida.date()}-{req.classe}"

        cached = self.repo.get_cache(chave)
        cache_status = "HIT" if cached else "MISS"

        if cached:
            voos_raw = cached
        else:
            alta_demanda = self._e_alta_demanda(req.data_ida)
            voos_raw = []
            for o in origens:
                for d in destinos:
                    voos_raw.extend(
                        gerar_voos(o, d, req.data_ida, req.adultos, req.classe, alta_demanda)
                    )
            if req.flex_dias > 0:
                for delta in range(-req.flex_dias, req.flex_dias + 1):
                    if delta == 0:
                        continue
                    data = req.data_ida + timedelta(days=delta)
                    for o in origens:
                        for d in destinos:
                            voos_raw.extend(
                                gerar_voos(o, d, data, req.adultos, req.classe,
                                           self._e_alta_demanda(data))
                            )
            self.repo.set_cache(chave, voos_raw)

        voos_raw = self._aplicar_filtros(voos_raw, req)
        voos_raw = self._ordenar(voos_raw, req.ordenar_por)

        if req.cadeirante:
            voos_raw = [v for v in voos_raw if v.get("cadeirante", True)]

        voos = [self._to_response(v, req.cadeirante) for v in voos_raw]

        sugestoes_datas, sugestoes_rotas = [], []
        melhor_data, menor_preco = None, None
        if not voos:
            event_bus.publish(Events.SEARCH_NO_RESULTS, {"origem": req.origem, "destino": req.destino})
            sugestoes_datas = [
                (req.data_ida + timedelta(days=d)).strftime("%Y-%m-%d") for d in [-1, 1, 2]
            ]
            sugestoes_rotas = [f"{req.origem}-BSB-{req.destino}"]
        else:
            menor_preco = min(v.preco for v in voos)
            melhor_data = min(voos, key=lambda x: x.preco).partida[:10]

        self.breaker.record_success()
        return BuscaResponse(
            voos=voos,
            total=len(voos),
            sugestoes_datas=sugestoes_datas,
            sugestoes_rotas=sugestoes_rotas,
            melhor_tarifa_data=melhor_data,
            menor_preco=menor_preco,
            cache=cache_status,
        )

    @staticmethod
    def _e_alta_demanda(data: datetime) -> bool:
        """Identifica períodos de alta demanda (Carnaval, férias, fim de ano)."""
        mes, dia = data.month, data.day
        # Carnaval / verão (fev), férias de julho, fim de ano e réveillon.
        if mes == 2 and dia >= 10:
            return True
        if mes == 7:
            return True
        if mes == 12 and dia >= 15:
            return True
        if mes == 1 and dia <= 7:
            return True
        return False

    def _aplicar_filtros(self, voos: list, req: BuscaRequest) -> list:
        result = voos
        if req.max_escalas is not None:
            result = [v for v in result if v["escalas"] <= req.max_escalas]
        if req.companhia:
            result = [v for v in result if v["companhia"] == req.companhia.upper()]
        if req.preco_max is not None:
            result = [v for v in result if v["preco"] <= req.preco_max]
        if req.preco_min is not None:
            result = [v for v in result if v["preco"] >= req.preco_min]
        return result

    def _ordenar(self, voos: list, criterio: str) -> list:
        if criterio == "preco":
            return sorted(voos, key=lambda v: v["preco"])
        if criterio == "duracao":
            return sorted(voos, key=lambda v: v["duracao_minutos"])
        if criterio == "partida":
            return sorted(voos, key=lambda v: v["partida"])
        return sorted(voos, key=lambda v: (v["preco"], v["duracao_minutos"]))

    def _to_response(self, v: dict, cadeirante: bool) -> VooResponse:
        from .schemas import CompanhiaInfo

        return VooResponse(
            id=v["id"],
            numero=v["numero"],
            companhia=CompanhiaInfo(**v["companhia"]),
            origem=v["origem"],
            destino=v["destino"],
            partida=v["partida"],
            chegada=v["chegada"],
            duracao_minutos=v["duracao_minutos"],
            escalas=v["escalas"],
            classe=v["classe"],
            preco=v["preco"],
            preco_por_passageiro=v["preco_por_passageiro"],
            preco_total=v["preco_total"],
            bagagem_inclusa=v["bagagem_inclusa"],
            bagagem_mao_kg=v.get("bagagem_mao_kg", 10),
            bagagem_despacho_kg=v.get("bagagem_despacho_kg", 0),
            alta_demanda=v.get("alta_demanda", False),
            special_assistance_required=cadeirante,
        )

    def listar_aeroportos(self, q: str = "") -> dict:
        from .gds_client import AEROPORTOS

        if q:
            resolved = resolver_aeroportos(q)
            return {"query": q, "aeroportos": resolved}
        return {"aeroportos": AEROPORTOS}

    def mapa_assentos(self, voo_id: str) -> dict:
        return {
            "voo_id": voo_id,
            "assentos": [
                {"codigo": f"{r}{c}", "disponivel": c not in (2, 5), "tipo": "standard"}
                for r in "ABCDEF" for c in range(1, 7)
            ],
        }
