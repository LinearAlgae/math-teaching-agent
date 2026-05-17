#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Math Teaching Agent - Setup Script"
echo "============================================"
echo ""

# ── Check prerequisites ────────────────────────────────

command -v python3 >/dev/null 2>&1 || { echo "ERROR: python3 is required but not installed."; exit 1; }

PY_VER=$(python3 --version 2>&1 | grep -Po '\d+\.\d+')
PY_MAJOR=$(echo "$PY_VER" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VER" | cut -d. -f2)
if [ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 11 ]; }; then
    echo "ERROR: Python 3.11+ required (found $PY_VER)"
    exit 1
fi
echo "  ✓ Python $PY_VER"

command -v uv >/dev/null 2>&1 || {
    echo ""
    echo "  ⚠  uv is not installed."
    echo "  Install it with:"
    echo "       curl -LsSf https://astral.sh/uv/install.sh | sh"
    echo "  or see: https://docs.astral.sh/uv/#installation"
    echo ""
    exit 1
}
echo "  ✓ uv"

command -v node >/dev/null 2>&1 || { echo "ERROR: node is required but not installed."; exit 1; }
NODE_VER=$(node --version | grep -Po '\d+' | head -1)
if [ "$NODE_VER" -lt 18 ]; then
    echo "ERROR: Node.js 18+ required (found $(node --version))"
    exit 1
fi
echo "  ✓ Node.js $(node --version)"

command -v npm >/dev/null 2>&1 || { echo "ERROR: npm is required but not installed."; exit 1; }
echo "  ✓ npm $(npm --version)"

echo ""
echo "── Checking optional system dependencies ──────────"
if command -v tesseract >/dev/null 2>&1; then
    echo "  ✓ tesseract (OCR)"
else
    echo "  ⚠  tesseract not found — OCR fallback may not work"
    echo "     Install: sudo apt install tesseract-ocr  (Linux)"
    echo "             brew install tesseract            (macOS)"
fi

echo ""
echo "── Setting up backend ─────────────────────────────"
cd "$ROOT_DIR/backend"

if [ -d ".venv" ]; then
    echo "  ◷  Virtual environment already exists, re-creating..."
    rm -rf .venv
fi

uv venv
echo "  ✓ Virtual environment created"

uv pip install -e .
echo "  ✓ Backend dependencies installed"

echo ""
echo "── Setting up frontend ────────────────────────────"
cd "$ROOT_DIR/frontend"

if [ -d "node_modules" ]; then
    echo "  ◷  node_modules already exists, updating..."
fi

npm install
echo "  ✓ Frontend dependencies installed"

echo ""
echo "============================================"
echo "  Setup complete!"
echo ""
echo "  Next steps:"
echo "    1. Start LM Studio and load a model on port 1234"
echo "    2. Run the app:  ./start.sh"
echo "    3. Open http://localhost:5173"
echo ""
echo "  Manual start:"
echo "    Backend:  cd backend && source .venv/bin/activate && uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000"
echo "    Frontend: cd frontend && npm run dev"
echo ""
echo "  Run tests:"
echo "    Backend:  cd backend && source .venv/bin/activate && uv run python -m pytest tests/"
echo "    Frontend: cd frontend && npx vitest run"
echo "============================================"
