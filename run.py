#!/usr/bin/env python3
"""
FINN: Cross-Platform Single Command Runner
Works on macOS, Linux, and Windows.
Launches both FastAPI Backend (port 8000) and Vite Frontend (port 3000).
"""

import sys
import os
import subprocess
import time
import signal
import shutil

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
BACKEND_DIR = os.path.join(ROOT_DIR, "backend")
FRONTEND_DIR = os.path.join(ROOT_DIR, "frontend")

IS_WINDOWS = sys.platform.startswith("win")
VENV_DIR = os.path.join(ROOT_DIR, ".venv")

if IS_WINDOWS:
    PYTHON_EXE = os.path.join(VENV_DIR, "Scripts", "python.exe")
    NPM_CMD = "npm.cmd"
else:
    PYTHON_EXE = os.path.join(VENV_DIR, "bin", "python3")
    NPM_CMD = "npm"

def setup_virtualenv():
    """Ensure .venv exists and has backend requirements installed."""
    # A .venv copied from another computer has a dead interpreter, so rebuild it
    if os.path.exists(VENV_DIR) and not os.path.exists(PYTHON_EXE):
        print("Existing .venv is not usable on this computer. Rebuilding it...")
        shutil.rmtree(VENV_DIR)

    if not os.path.exists(VENV_DIR):
        print("Creating Python virtual environment (.venv)...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])
        print("Installing backend dependencies...")
        req_file = os.path.join(BACKEND_DIR, "requirements.txt")
        subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-r", req_file])
    else:
        # Check if uvicorn is installed
        try:
            subprocess.check_call([PYTHON_EXE, "-c", "import uvicorn, fastapi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            print("Installing/updating backend dependencies in .venv...")
            req_file = os.path.join(BACKEND_DIR, "requirements.txt")
            subprocess.check_call([PYTHON_EXE, "-m", "pip", "install", "-r", req_file])

def setup_frontend():
    """Ensure frontend dependencies are installed."""
    node_modules = os.path.join(FRONTEND_DIR, "node_modules")
    if not os.path.exists(node_modules):
        print("Installing frontend dependencies (npm install)...")
        npm_path = shutil.which(NPM_CMD) or shutil.which("npm")
        if not npm_path:
            print("WARNING: 'npm' was not found in your PATH. Please install Node.js (https://nodejs.org).")
            return
        subprocess.check_call([npm_path, "install"], cwd=FRONTEND_DIR)

def main():
    if sys.version_info < (3, 10):
        sys.exit("FINN needs Python 3.10 or newer. Try: python3.12 run.py")

    print("=" * 70)
    print("  ⚡ Starting FINN: Financial Investment Agent (NSE / BSE Intelligence)")
    print("=" * 70)

    # 1. Setup Environments
    setup_virtualenv()
    setup_frontend()

    # Set PYTHONPATH to include backend directory
    env = os.environ.copy()
    current_pp = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = f"{BACKEND_DIR}{os.pathsep}{current_pp}" if current_pp else BACKEND_DIR

    processes = []

    try:
        # 2. Start Backend Server
        print("\nStarting FastAPI backend server on http://localhost:8000...")
        backend_proc = subprocess.Popen(
            [PYTHON_EXE, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
            cwd=ROOT_DIR,
            env=env
        )
        processes.append(backend_proc)

        # Wait a moment for backend startup
        time.sleep(1.5)

        # 3. Start Frontend Server
        npm_path = shutil.which(NPM_CMD) or shutil.which("npm")
        if npm_path:
            print("Starting Vite frontend server on http://localhost:3000...")
            frontend_proc = subprocess.Popen(
                [npm_path, "run", "dev", "--", "--host"],
                cwd=FRONTEND_DIR
            )
            processes.append(frontend_proc)
        else:
            print("\nNOTE: Could not launch frontend automatically because npm was not found.")
            print("To run frontend manually: cd frontend && npm install && npm run dev")

        print("\n" + "=" * 70)
        print("  🚀 FINN is running:")
        print("     • Frontend Web App:  http://localhost:3000")
        print("     • Backend API Docs:  http://localhost:8000/docs")
        print("     • Health Endpoint:   http://localhost:8000/api/health")
        print("=" * 70)
        print("  Press Ctrl+C to stop both servers.\n")

        # Keep running until user terminates
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nShutting down FINN backend and frontend...")
    finally:
        for p in processes:
            try:
                p.terminate()
                p.wait(timeout=3)
            except Exception:
                p.kill()
        print("All servers stopped successfully. Goodbye!")

if __name__ == "__main__":
    main()

