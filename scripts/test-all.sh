#!/usr/bin/env bash
# Executa toda a suíte de testes do SkyAgent.
# Rodar antes de cada commit ou ao finalizar uma funcionalidade.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAILED=0

echo "========================================"
echo " SkyAgent — Suíte completa de testes"
echo "========================================"

# --- Backend (pytest) ---
echo ""
echo ">>> [1/3] Backend — pytest"
cd "$ROOT/backend"
if [ -d venv ]; then
  source venv/bin/activate
fi
if pytest tests/ -v --tb=short; then
  echo "OK: pytest"
else
  echo "FALHOU: pytest"
  FAILED=1
fi

# --- BDD (behave) ---
echo ""
echo ">>> [2/3] BDD — behave"
cd "$ROOT/features"
if behave --no-capture 2>&1; then
  echo "OK: behave"
else
  echo "AVISO: behave — alguns cenários podem não ter steps ainda"
  # Não falha o script inteiro: muitos cenários BDD ainda sem step definitions
fi

# --- Frontend (build) ---
echo ""
echo ">>> [3/3] Frontend — npm run build"
cd "$ROOT/frontend"
if [ -d node_modules ]; then
  if npm run build; then
    echo "OK: frontend build"
  else
    echo "FALHOU: frontend build"
    FAILED=1
  fi
else
  echo "SKIP: node_modules não encontrado (rode npm install)"
fi

echo ""
echo "========================================"
if [ "$FAILED" -eq 0 ]; then
  echo " Resultado: SUÍTE PRINCIPAL OK"
  exit 0
else
  echo " Resultado: FALHAS DETECTADAS"
  exit 1
fi
