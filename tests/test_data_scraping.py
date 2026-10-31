"""
Data Scraping Verification Script
Demonstrating the 3 guided backend data sources from the challenge brief:
  1. Price & volume (EOD) scrapable from public sources (Yahoo Finance / yfinance)
  2. Corporate announcements / filings from NSE/BSE
  3. Company fundamentals (annual reports & concall transcript links) from screener.in
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.services.data_fetchers.yfinance_client import eod_service
from app.services.data_fetchers.nse_bse_filings import filings_service
from app.services.data_fetchers.screener_scraper import screener_service

def verify_price_volume_scraping():
    print("\n--- 1. Testing Price & Volume EOD Scraper (yfinance) ---")
    ticker = "TRENT"
    data = eod_service.fetch_stock_eod(ticker, vol_threshold=2.0, price_threshold=4.0)
    print(f"Ticker: {data['ticker']} ({data['symbol']})")
    print(f"Close Price: ₹{data['close']:,.2f} (Day Change: {data['pct_change']}%)")
    print(f"Volume: {data['volume']:,} shares (20d Avg: {data['avg_volume_20d']:,})")
    print(f"Volume Multiple: {data['volume_multiple']}x (Unusual Spike: {data['is_unusual_volume']})")
    assert "close" in data and "volume_multiple" in data
    print("✓ Price & Volume Scraping Component Operational")

def verify_filings_scraping():
    print("\n--- 2. Testing Corporate Announcements & Filings Scraper (NSE/BSE) ---")
    announcements = filings_service.get_announcements(window_hours=48)
    print(f"Total Ingested Announcements: {len(announcements)}")
    sample = announcements[0]
    print(f"Sample Filing: [{sample.category}] {sample.ticker} - {sample.headline}")
    print(f"Priority Level: {sample.priority.value} | Summary: {sample.one_line_summary}")
    assert len(announcements) > 0
    print("✓ Corporate Announcements Ingestion Component Operational")

def verify_screener_fundamentals_scraping():
    print("\n--- 3. Testing Screener.in Fundamentals & Document Scraper ---")
    ticker = "TRENT"
    fundamentals = screener_service.get_company_fundamentals(ticker)
    fin = fundamentals["financial_snapshot"]
    print(f"Company: {fundamentals['company_name']} ({fundamentals['ticker']})")
    print(f"TTM Revenue: ₹{fin['ttm_revenue_cr']:,} Cr | EBITDA Margin: {fin['ebitda_margin_pct']}%")
    print(f"ROCE: {fin['roce_pct']}% | ROE: {fin['roe_pct']}% | P/E: {fin['pe_ratio']}x")
    print(f"Primary Source Footnote: {fin['primary_source_notes']}")
    assert fin["ttm_revenue_cr"] > 0
    print("✓ Screener.in Fundamentals & Primary Document Link Scraper Operational")

if __name__ == "__main__":
    print("=================================================================")
    print("   VERIFYING 3 GUIDED DATA SCRAPING SOURCES (ENAM AI CHALLENGE)   ")
    print("=================================================================")
    verify_price_volume_scraping()
    verify_filings_scraping()
    verify_screener_fundamentals_scraping()
    print("\n================ ALL 3 DATA SOURCES VERIFIED SUCCESSFULLY ================\n")

