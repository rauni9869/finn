from fastapi import APIRouter, Query
from typing import Optional
from app.models.schemas import WindowedDigestResponse, AlertThresholdConfig
from app.services.push.digest_aggregator import digest_service

router = APIRouter(prefix="/digest", tags=["Digest"])

@router.get("", response_model=WindowedDigestResponse)
def get_windowed_digest(
    window_hours: int = Query(24, ge=1, le=168, description="Time window in hours (default 24h)"),
    ticker: Optional[str] = Query(None, description="Optional filter by ticker symbol"),
    vol_thresh: float = Query(2.0, ge=1.0, le=10.0, description="Volume multiplier threshold"),
    price_thresh: float = Query(4.0, ge=0.5, le=20.0, description="Price change percentage threshold")
):
    """Retrieve filtered and prioritized windowed digest across the portfolio."""
    cfg = AlertThresholdConfig(
        volume_multiplier_threshold=vol_thresh,
        price_change_pct_threshold=price_thresh
    )
    return digest_service.get_digest(
        window_hours=window_hours,
        ticker=ticker,
        threshold_config=cfg
    )

