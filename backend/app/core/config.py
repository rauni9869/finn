import os
from pathlib import Path
from typing import List, Dict
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
BACKEND_DIR = BASE_DIR / "backend"
DATA_DIR = BASE_DIR / "data"
SEED_DIR = DATA_DIR / "seed"
CACHE_DIR = DATA_DIR / "cache"

# Ensure directories exist
SEED_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

class Settings(BaseModel):
    PROJECT_NAME: str = "FINN: Financial Investment Agent"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    MOCK_MODE_DEFAULT: bool = False  # Set to False so live scrapers run by default with fallback
    ENABLE_LIVE_SCRAPING: bool = os.getenv("ENABLE_LIVE_SCRAPING", "true").lower() in ("true", "1")

settings = Settings()

# 18 Mock Portfolio Stocks (Large, Mid, Small, Micro across sectors)
PORTFOLIO_STOCKS: List[Dict[str, str]] = [
    {"ticker": "RELIANCE", "symbol": "RELIANCE.NS", "name": "Reliance Industries Ltd", "sector": "Energy / Conglomerate", "market_cap": "Mega Cap"},
    {"ticker": "HDFCBANK", "symbol": "HDFCBANK.NS", "name": "HDFC Bank Ltd", "sector": "Banking / Financials", "market_cap": "Large Cap"},
    {"ticker": "TCS", "symbol": "TCS.NS", "name": "Tata Consultancy Services Ltd", "sector": "IT Services", "market_cap": "Large Cap"},
    {"ticker": "TATAMOTORS", "symbol": "TATAMOTORS.NS", "name": "Tata Motors Ltd", "sector": "Automobile / EV", "market_cap": "Large Cap"},
    {"ticker": "SUNPHARMA", "symbol": "SUNPHARMA.NS", "name": "Sun Pharmaceutical Industries Ltd", "sector": "Pharmaceuticals", "market_cap": "Large Cap"},
    {"ticker": "LT", "symbol": "LT.NS", "name": "Larsen & Toubro Ltd", "sector": "Infrastructure / EPC", "market_cap": "Large Cap"},
    {"ticker": "TITAN", "symbol": "TITAN.NS", "name": "Titan Company Ltd", "sector": "Consumer Discretionary", "market_cap": "Large Cap"},
    {"ticker": "ITC", "symbol": "ITC.NS", "name": "ITC Ltd", "sector": "FMCG / Diversified", "market_cap": "Large Cap"},
    {"ticker": "PERSISTENT", "symbol": "PERSISTENT.NS", "name": "Persistent Systems Ltd", "sector": "Mid-Cap IT", "market_cap": "Mid Cap"},
    {"ticker": "POLYCAB", "symbol": "POLYCAB.NS", "name": "Polycab India Ltd", "sector": "Cables & EPC", "market_cap": "Mid Cap"},
    {"ticker": "TRENT", "symbol": "TRENT.NS", "name": "Trent Ltd", "sector": "Retail / Fast Fashion", "market_cap": "Mid Cap"},
    {"ticker": "FEDERALBNK", "symbol": "FEDERALBNK.NS", "name": "Federal Bank Ltd", "sector": "Private Banking", "market_cap": "Mid Cap"},
    {"ticker": "DEEPAKNTR", "symbol": "DEEPAKNTR.NS", "name": "Deepak Nitrite Ltd", "sector": "Specialty Chemicals", "market_cap": "Mid Cap"},
    {"ticker": "KAYNES", "symbol": "KAYNES.NS", "name": "Kaynes Technology India Ltd", "sector": "EMS / Electronics", "market_cap": "Small/Mid Cap"},
    {"ticker": "ZENTEC", "symbol": "ZENTEC.NS", "name": "Zen Technologies Ltd", "sector": "Defence Simulation", "market_cap": "Small Cap"},
    {"ticker": "SUPRIYA", "symbol": "SUPRIYA.NS", "name": "Supriya Lifescience Ltd", "sector": "Pharma / API", "market_cap": "Small Cap"},
    {"ticker": "ETHOSLTD", "symbol": "ETHOSLTD.NS", "name": "Ethos Ltd", "sector": "Luxury Retail", "market_cap": "Small Cap"},
    {"ticker": "KSOLVES", "symbol": "KSOLVES.NS", "name": "Ksolves India Ltd", "sector": "Micro-Cap IT", "market_cap": "Micro Cap"}
]

# 4 Ad-hoc out-of-portfolio tickers to verify dynamic generalisation
AD_HOC_STOCKS: List[Dict[str, str]] = [
    {"ticker": "DIXON", "symbol": "DIXON.NS", "name": "Dixon Technologies Ltd", "sector": "EMS / Manufacturing", "market_cap": "Mid Cap"},
    {"ticker": "ZOMATO", "symbol": "ZOMATO.NS", "name": "Zomato Ltd", "sector": "Consumer Internet / Quick Commerce", "market_cap": "Large Cap"},
    {"ticker": "CDSL", "symbol": "CDSL.NS", "name": "Central Depository Services Ltd", "sector": "Capital Markets Infrastructure", "market_cap": "Mid Cap"},
    {"ticker": "SUZLON", "symbol": "SUZLON.NS", "name": "Suzlon Energy Ltd", "sector": "Renewable Energy / Wind", "market_cap": "Mid Cap"}
]

