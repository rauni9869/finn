#!/usr/bin/env bash
# ==============================================================================
# FINN: Financial Investment Agent — Single Command Orchestrator
# ENAM Holdings AI Engineer Build Challenge
# ==============================================================================

set -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd "$DIR"

echo "======================================================================="
echo "  ⚡ Starting FINN: Financial Investment Agent (NSE / BSE Intelligence)"
echo "======================================================================="

# Verify / Setup Python virtualenv
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment (.venv)..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r backend/requirements.txt
else
    source .venv/bin/activate
fi

export PYTHONPATH="${DIR}/backend:${PYTHONPATH:-}"

# Function to kill child processes on exit
cleanup() {
    echo ""
    echo "Shutting down FINN backend and frontend services..."
    if [ ! -z "$BACKEND_PID" ]; then
        kill "$BACKEND_PID" 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill "$FRONTEND_PID" 2>/dev/null || true
    fi
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# 1. Start FastAPI Backend
echo "Starting FastAPI backend server on http://localhost:8000..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Wait for backend health check
echo "Waiting for backend to be healthy..."
for i in {1..30}; do
    if curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "✓ Backend is UP and healthy on http://localhost:8000"
        break
    fi
    sleep 0.5
done

# 2. Start Vite Frontend
echo "Starting Vite frontend server on http://localhost:5173..."
cd frontend
npm run dev -- --host &
FRONTEND_PID=$!
cd ..

echo "======================================================================="
echo "  🚀 FINN is LIVE:"
echo "     • Frontend Web App:  http://localhost:5173"
echo "     • Backend API Docs:  http://localhost:8000/docs"
echo "     • Health Endpoint:   http://localhost:8000/api/health"
echo "======================================================================="
echo "  Press Ctrl+C to stop both servers."

wait
