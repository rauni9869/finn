# FINN: Financial Investment Agent (NSE / BSE)

A mobile-first prototype for the ENAM Holdings AI Engineer Build Challenge. FINN tells an investor what changed (**Push**) and shows a research view of a company on demand (**Pull**).

## What is live and what is sample data

| Area | Status |
|---|---|
| End-of-day prices, volume and threshold alerts | **Live** from Yahoo Finance. A stock shows "Unavailable" if Yahoo has no data for its symbol. |
| Financial figures and annual report / concall links for any NSE ticker | **Live** from screener.in. |
| Corporate filings in the digest | **Sample data**: 20 hand-written filings. The window is measured back from the newest one. A live NSE fetch exists in the code but is not connected. |
| Management bio and results scorecard | **Sample data**, attached to the sample filings. |
| Narrative vs Numbers, Bull vs Bear, Balance Sheet, Cash Quality, Guidance | **Hand-written sample profiles** for TRENT, TATAMOTORS, POLYCAB, DIXON and ZOMATO. They have not been checked against the filings. Other tickers show "Not assessed". |
| LLM analysis | **Not connected.** `backend/app/services/llm/router.py` is a Gemini client that nothing calls yet. |

An unknown ticker returns "No data found" rather than an invented report.

## Features

**Push**
- Digest with 24 hour, 48 hour and 7 day windows, sorted by priority then newest first
- Routine filings collapsed into a drawer
- The 17 filing categories from the challenge reference
- Volume and price alerts with adjustable sliders
- "Why Care?" notes on each filing
- A browser-spoken audio briefing

**Pull**
- Search any NSE ticker for live figures and primary document links
- Seven research tabs for the sample profiles, including promises vs delivery

## Run it

Requires Python 3.10+ and Node.js 18+.

```bash
python3.12 run.py
```

Then open **http://localhost:3000**. API docs are at http://localhost:8000/docs. Press `Ctrl+C` to stop.

The launcher creates `.venv` and installs dependencies on the first run. See [SETUP_GUIDE.md](SETUP_GUIDE.md) for details.

## Tests

```bash
PYTHONPATH=backend .venv/bin/python tests/test_e2e.py
PYTHONPATH=backend .venv/bin/python tests/test_data_scraping.py
```

Both call Yahoo Finance and screener.in, so they need internet access.

## Deploy

`render.yaml` builds the frontend and serves it from FastAPI as one web service. Create a Render Blueprint from the GitHub repository. Render's free tier sleeps when idle, so the first request can be slow.

## Structure

```
├── run.py, run.sh            # Start backend and frontend
├── render.yaml               # Single-service deployment
├── covering_note.md          # Draft submission writeup
├── tests/
├── backend/app/
│   ├── main.py               # API entry point; also serves frontend/dist when built
│   ├── core/config.py        # Portfolio and ad-hoc stock lists
│   ├── models/schemas.py     # Data shapes
│   ├── api/routes/           # portfolio, digest, alerts, research
│   └── services/
│       ├── data_fetchers/    # Yahoo, screener.in, sample filings and profiles
│       ├── push/             # Classifier, alerts, digest
│       ├── pull/             # Research report assembly
│       └── llm/              # Unused Gemini client
└── frontend/src/
    ├── App.tsx, api.ts, types/
    └── components/           # Header, BottomNav, PushDigestFeed, PullResearchHub,
                              # PortfolioWatch, AlertSliderModal, AudioBriefingModal
```

## Known limitations

- `TATAMOTORS.NS` no longer returns data on Yahoo Finance, so that stock shows "Unavailable" in the Universe tab.
- The classifier is keyword-based and misses some cases, such as labelling an auditor appointment as a management change. It does not affect the sample filings, which carry their own labels.
- The sample profiles cover Q3 FY24 to Q2 FY25, so they are out of date.
