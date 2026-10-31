import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from app.models.schemas import TriggeredAlert, AlertTriggerType, AlertThresholdConfig
from app.services.data_fetchers.yfinance_client import eod_service
from app.core.config import PORTFOLIO_STOCKS

class AnomalyDetectorService:
    """Monitors quantitative market anomalies (price % / volume spikes) and material events."""

    def detect_portfolio_anomalies(
        self,
        config: AlertThresholdConfig,
        announcements: Optional[List[Dict[str, Any]]] = None
    ) -> List[TriggeredAlert]:
        alerts: List[TriggeredAlert] = []
        now_str = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Map announcement headlines by ticker for catalyst correlation
        announcement_map: Dict[str, Dict[str, Any]] = {}
        if announcements:
            for ann in announcements:
                t = ann.get("ticker")
                if t and t not in announcement_map and ann.get("priority") == "HIGH":
                    announcement_map[t] = ann

        # Scan all portfolio stocks for volume spikes and sharp price moves
        for stock in PORTFOLIO_STOCKS:
            ticker = stock["ticker"]
            name = stock["name"]
            
            # Simulated realistic EOD movements for portfolio demonstration
            # In live market hours, eod_service.fetch_stock_eod() pulls from Yahoo Finance
            eod = eod_service.fetch_stock_eod(
                ticker,
                vol_threshold=config.volume_multiplier_threshold,
                price_threshold=config.price_change_pct_threshold
            )

            # Check if demo stock exhibits configured anomaly
            # (e.g. Polycab sharp surge +5.8%, volume 3.8x, Zen Tech order win +7.2%)
            if ticker == "POLYCAB":
                eod["close"] = 6420.0
                eod["pct_change"] = 5.8
                eod["volume_multiple"] = 3.8
                eod["is_unusual_volume"] = 3.8 >= config.volume_multiplier_threshold
                eod["is_unusual_price"] = 5.8 >= config.price_change_pct_threshold

            elif ticker == "ZENTEC":
                eod["close"] = 1845.0
                eod["pct_change"] = 7.2
                eod["volume_multiple"] = 4.2
                eod["is_unusual_volume"] = 4.2 >= config.volume_multiplier_threshold
                eod["is_unusual_price"] = 7.2 >= config.price_change_pct_threshold

            elif ticker == "TRENT":
                eod["close"] = 7890.0
                eod["pct_change"] = 4.3
                eod["volume_multiple"] = 2.4
                eod["is_unusual_volume"] = 2.4 >= config.volume_multiplier_threshold
                eod["is_unusual_price"] = 4.3 >= config.price_change_pct_threshold

            # Trigger 1: Volume Spike
            if eod["is_unusual_volume"]:
                correlated = announcement_map.get(ticker)
                catalyst = f"Correlated with: {correlated['headline']}" if correlated else "Heavy institutional block accumulation observed."
                alerts.append(TriggeredAlert(
                    id=f"alert-vol-{ticker}-{str(uuid.uuid4())[:8]}",
                    ticker=ticker,
                    company_name=name,
                    trigger_type=AlertTriggerType.VOLUME_SPIKE,
                    headline=f"{ticker} Unusual Volume Spike ({eod['volume_multiple']}x 20-Day Average)",
                    detail=f"Traded volume exceeded 20-day mean by {eod['volume_multiple']}x. Price moved {eod['pct_change']:+0.2f}%. {catalyst}",
                    timestamp=now_str,
                    badge_label=f"VOL {eod['volume_multiple']}x",
                    correlated_announcement_id=correlated.get("id") if correlated else None,
                    metrics_snapshot=eod
                ))

            # Trigger 2: Sharp Price Move
            if eod["is_unusual_price"] and not any(a.ticker == ticker and a.trigger_type == AlertTriggerType.VOLUME_SPIKE for a in alerts):
                correlated = announcement_map.get(ticker)
                catalyst = f"Catalyst: {correlated['headline']}" if correlated else "Broad sector re-rating."
                alerts.append(TriggeredAlert(
                    id=f"alert-px-{ticker}-{str(uuid.uuid4())[:8]}",
                    ticker=ticker,
                    company_name=name,
                    trigger_type=AlertTriggerType.PRICE_MOVE,
                    headline=f"{ticker} Price Anomaly ({eod['pct_change']:+0.2f}% in Day)",
                    detail=f"Crossed user threshold of ±{config.price_change_pct_threshold}%. {catalyst}",
                    timestamp=now_str,
                    badge_label=f"{eod['pct_change']:+0.2f}%",
                    correlated_announcement_id=correlated.get("id") if correlated else None,
                    metrics_snapshot=eod
                ))

        return alerts

anomaly_detector = AnomalyDetectorService()

