from typing import Optional
from app.models.schemas import WindowedDigestResponse, AlertThresholdConfig, PriorityLevel
from app.services.data_fetchers.nse_bse_filings import filings_service
from app.services.push.anomaly_detector import anomaly_detector

class DigestAggregatorService:
    """Aggregates windowed corporate filings and quantitative alerts for the mobile push feed."""

    def get_digest(
        self,
        window_hours: int = 24,
        ticker: Optional[str] = None,
        threshold_config: Optional[AlertThresholdConfig] = None
    ) -> WindowedDigestResponse:
        cfg = threshold_config or AlertThresholdConfig()

        # Retrieve classified and prioritized corporate announcements
        announcements = filings_service.get_announcements(
            ticker=ticker,
            window_hours=window_hours,
            include_collapsed=True
        )

        # Detect active alerts across the portfolio based on slider thresholds
        dict_announcements = [ann.model_dump() for ann in announcements]
        active_alerts = anomaly_detector.detect_portfolio_anomalies(
            config=cfg,
            announcements=dict_announcements
        )

        # Compute summary counts
        high_priority_count = sum(1 for a in announcements if a.priority == PriorityLevel.HIGH)
        routine_collapsed_count = sum(1 for a in announcements if a.priority == PriorityLevel.LOW)

        return WindowedDigestResponse(
            window_hours=window_hours,
            total_announcements=len(announcements),
            high_priority_count=high_priority_count,
            routine_collapsed_count=routine_collapsed_count,
            announcements=announcements,
            active_alerts=active_alerts,
            is_sample_data=True,
            data_as_of=filings_service.sample_data_as_of().strftime("%Y-%m-%dT%H:%M:%SZ")
        )

digest_service = DigestAggregatorService()

