from fastapi import APIRouter
from typing import List
from app.models.schemas import StockInfo, EODMetrics
from app.core.config import PORTFOLIO_STOCKS, AD_HOC_STOCKS
from app.services.data_fetchers.yfinance_client import eod_service

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])

@router.get("", response_model=List[StockInfo])
def get_portfolio():
    """Retrieve the 18 high-conviction portfolio companies with latest EOD market metrics."""
    result: List[StockInfo] = []
    for s in PORTFOLIO_STOCKS:
        eod_dict = eod_service.fetch_stock_eod(s["ticker"])
        
        eod_metric = EODMetrics(**eod_dict) if eod_dict else None
        result.append(StockInfo(
            ticker=s["ticker"],
            symbol=s["symbol"],
            name=s["name"],
            sector=s["sector"],
            market_cap=s["market_cap"],
            is_portfolio=True,
            eod=eod_metric
        ))
    return result

@router.get("/universe", response_model=List[StockInfo])
def get_universe():
    """Returns combined universe of portfolio stocks + ad-hoc research test stocks."""
    result: List[StockInfo] = []
    
    # Portfolio stocks
    for s in PORTFOLIO_STOCKS:
        eod_dict = eod_service.fetch_stock_eod(s["ticker"])
        eod_metric = EODMetrics(**eod_dict) if eod_dict else None
        result.append(StockInfo(
            ticker=s["ticker"],
            symbol=s["symbol"],
            name=s["name"],
            sector=s["sector"],
            market_cap=s["market_cap"],
            is_portfolio=True,
            eod=eod_metric
        ))
        
    # Ad-hoc stocks
    for s in AD_HOC_STOCKS:
        eod_dict = eod_service.fetch_stock_eod(s["ticker"])
        eod_metric = EODMetrics(**eod_dict) if eod_dict else None
        result.append(StockInfo(
            ticker=s["ticker"],
            symbol=s["symbol"],
            name=s["name"],
            sector=s["sector"],
            market_cap=s["market_cap"],
            is_portfolio=False,
            eod=eod_metric
        ))
        
    return result

