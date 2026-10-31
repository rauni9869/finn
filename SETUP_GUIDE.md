# FINN: Setup Guide

## You need
- Python 3.10 or newer (`python3.12 --version`)
- Node.js 18 or newer (`node -v`)

## Start the app

From the project folder:

```bash
python3.12 run.py
```

On Windows, use `python run.py`.

The first run takes 1–2 minutes because it installs everything. Open **http://localhost:3000** when you see `Local: http://localhost:3000/`. The first load can take about 30 seconds while prices download.

Press `Ctrl+C` in the terminal to stop.

## Start the two servers separately

**Backend (terminal 1, from the project folder):**
```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
PYTHONPATH=backend python -m uvicorn app.main:app --port 8000 --reload
```

**Frontend (terminal 2):**
```bash
cd frontend
npm install
npm run dev
```

## Try it on a phone

Connect your phone and computer to the same Wi-Fi, then find your computer's address:

```bash
ipconfig getifaddr en0
```

Open `http://THAT_ADDRESS:3000` on your phone. For a quick check on a computer, use your browser's device toolbar instead.

## Troubleshooting

| Problem | Fix |
|---|---|
| Port already in use | `kill $(lsof -ti:8000,3000)` |
| `Operation not permitted` or `library load disallowed` on a Mac | The copied `node_modules` is quarantined. Run `rm -rf frontend/node_modules` and start again. |
| Connection error on the page | The backend is still starting. Wait a few seconds and click **Retry**. |
| A stock shows "Unavailable" | Yahoo Finance has no data for that symbol right now. |
| "No data found" for a ticker | The ticker is wrong, or screener.in can't be reached. |

See [README.md](README.md) for what is live and what is sample data.
