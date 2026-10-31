from fastapi import APIRouter
from typing import List
from app.models.schemas import TriggeredAlert, AlertThresholdConfig
from app.services.push.anomaly_detector import anomaly_detector
from app.services.data_fetchers.seed_data import SEED_ANNOUNCEMENTS

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("", response_model=List[TriggeredAlert])
def get_active_alerts():
    """Retrieve all triggered market alerts based on default thresholds."""
    config = AlertThresholdConfig()
    return anomaly_detector.detect_portfolio_anomalies(
        config=config,
        announcements=SEED_ANNOUNCEMENTS
    )

@router.post("/evaluate", response_model=List[TriggeredAlert])
def evaluate_custom_thresholds(config: AlertThresholdConfig):
    """Dynamically re-evaluates market moves and filings against user slider thresholds."""
    return anomaly_detector.detect_portfolio_anomalies(
        config=config,
        announcements=SEED_ANNOUNCEMENTS
    )

