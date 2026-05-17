#!/usr/bin/env bash
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================"
echo "  Math Teaching Agent - Launch Script"
echo "============================================"
echo ""

# ── Check LM Studio ──────────────────────────────────────────
echo "[1/4] Checking LM Studio..."
if curl -s --max-time 3 http://127.0.0.1:1234/api/v1/models > /dev/null 2>&1; then
    echo "  ✓ LM Studio is running on http://127.0.0.1:1234"
else
    echo ""
    echo "  ⚠  LM Studio is NOT running!"
    echo "  Please start LM Studio and load a model first."
    echo "  (e.g. google/gemma-4-e4b or qwen3.5-4b)"
    echo "  Then re-run this script."
    echo ""
    exit 1
fi

# ── Kill existing processes ──────────────────────────────────
echo "[2/4] Stopping any existing backend/frontend..."
fuser -k 8000/tcp 2>/dev/null || true
fuser -k 5173/tcp 2>/dev/null || true
sleep 1
echo "  ✓ Ports 8000 and 5173 are free"

# ── Start backend ────────────────────────────────────────────
echo "[3/4] Starting backend (uvicorn)..."
cd "$ROOT_DIR/backend"
.venv/bin/uvicorn src.main:app --host 0.0.0.0 --port 8000 > /tmp/math-agent-backend.log 2>&1 &
BACKEND_PID=$!
echo "  ✓ Backend started (PID $BACKEND_PID) — http://127.0.0.1:8000"

# ── Start frontend ───────────────────────────────────────────
echo "[4/4] Starting frontend (vite)..."
cd "$ROOT_DIR/frontend"
npm run dev > /tmp/math-agent-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "  ✓ Frontend started (PID $FRONTEND_PID) — http://127.0.0.1:5173"

echo ""
echo "============================================"
echo "  App is ready!"
echo ""
echo "  Open in your browser:"
echo "    → http://localhost:5173"
echo ""
echo "  Logs:"
echo "    Backend  → tail -f /tmp/math-agent-backend.log"
echo "    Frontend → tail -f /tmp/math-agent-frontend.log"
echo ""
echo "  To stop:  fuser -k 8000/tcp && fuser -k 5173/tcp"
echo "============================================"