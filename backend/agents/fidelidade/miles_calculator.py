"""Cálculo de milhas."""
MULTIPLICADORES = {"Bronze": 1, "Prata": 1.25, "Ouro": 1.5, "Diamante": 2}
NIVEIS = ["Bronze", "Prata", "Ouro", "Diamante"]
LIMIARES = {"Bronze": 0, "Prata": 10000, "Ouro": 25000, "Diamante": 50000}


def calcular_milhas(valor: float, nivel: str) -> int:
    base = int(valor / 10)
    return int(base * MULTIPLICADORES.get(nivel, 1))
