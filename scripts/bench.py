"""Benchmark de tempo de resposta dos endpoints do SkyAgent.

Uso: python scripts/bench.py [base_url] [repeticoes]
"""
import statistics
import sys
import time
from datetime import datetime, timedelta, timezone

import httpx

BASE = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
N = int(sys.argv[2]) if len(sys.argv) > 2 else 30

data_ida = (datetime.now(timezone.utc) + timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")

# (rotulo, metodo, path, params, json_body)
ENDPOINTS = [
    ("health", "GET", "/health", None, None),
    ("pipeline.health", "GET", "/api/pipeline/health", None, None),
    ("voos.aeroportos", "GET", "/api/voos/aeroportos", {"q": "sao paulo"}, None),
    ("voos.buscar (cache HIT)", "GET", "/api/voos/buscar",
     {"origem": "GRU", "destino": "GIG", "data_ida": data_ida}, None),
    ("voos.buscar (flex=3)", "GET", "/api/voos/buscar",
     {"origem": "GRU", "destino": "GIG", "data_ida": data_ida, "flex_dias": 3}, None),
    ("voos.assentos", "GET", "/api/voos/ABC-20260101/assentos", None, None),
    ("preco.calcular", "POST", "/api/preco/calcular", None,
     {"voo_id": "LA3421-20260101", "preco_base": 500.0, "adultos": 1}),
    ("preco.cupom.validar", "POST", "/api/preco/cupom/validar", None,
     {"codigo": "VERAO20", "valor_compra": 500.0}),
    ("marketing.metricas", "GET", "/api/marketing/metricas", None, None),
    ("fidelidade.saldo", "GET", "/api/fidelidade/CLI123/saldo", None, None),
    ("fidelidade.nivel", "GET", "/api/fidelidade/CLI123/nivel", None, None),
    ("atendimento.chat (LLM/FAQ)", "POST", "/api/atendimento/chat", None,
     {"mensagem": "Qual a politica de bagagem?", "canal": "web"}),
]


def medir(client, method, path, params, body):
    tempos = []
    erros = 0
    status = None
    for _ in range(N):
        t0 = time.perf_counter()
        try:
            r = client.request(method, BASE + path, params=params, json=body, timeout=40)
            status = r.status_code
            if r.status_code >= 400:
                erros += 1
        except Exception:
            erros += 1
            continue
        tempos.append((time.perf_counter() - t0) * 1000)
    return tempos, erros, status


def pct(vals, p):
    if not vals:
        return 0.0
    s = sorted(vals)
    k = int(round((p / 100) * (len(s) - 1)))
    return s[k]


def main():
    print(f"Benchmark SkyAgent — base={BASE} repeticoes={N}\n")
    header = f"{'endpoint':<30}{'status':>7}{'min':>9}{'media':>9}{'p50':>9}{'p95':>9}{'max':>9}{'err':>5}"
    print(header)
    print("-" * len(header))
    rows = []
    with httpx.Client() as client:
        for label, method, path, params, body in ENDPOINTS:
            tempos, erros, status = medir(client, method, path, params, body)
            if tempos:
                row = (label, status, min(tempos), statistics.mean(tempos),
                       pct(tempos, 50), pct(tempos, 95), max(tempos), erros)
            else:
                row = (label, status, 0, 0, 0, 0, 0, erros)
            rows.append(row)
            print(f"{label:<30}{str(status):>7}{row[2]:>9.1f}{row[3]:>9.1f}"
                  f"{row[4]:>9.1f}{row[5]:>9.1f}{row[6]:>9.1f}{erros:>5}")
    print("\n(valores em ms)")


if __name__ == "__main__":
    main()
