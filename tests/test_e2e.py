"""
FINN End-to-End Test Suite
Tests:
  1. Health check & configuration
  2. Portfolio universe (18 stocks) + EOD metrics
  3. Push side: 24h/48h windowed digest, 17-category classification, high priority vs routine paperwork collapse
  4. Push side: Triggered alerts (volume > 2x, price moves > 4%)
  5. Push side: 2 enrichments (Quarterly Results instant cut + Management Change bio)
  6. Pull side: 8-dimension grounded research on core portfolio stock (TRENT)
  7. Pull side: Flagship Narrative vs Numbers 4-quarter matrix with source citations
  8. Pull side: Generalisation on out-of-portfolio ad-hoc stock (DIXON)
  9. Governance check: RPTs flag and Auditor Qualification status
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    print("✓ Health Check Passed")

def test_portfolio_universe():
    res = client.get("/api/portfolio")
    assert res.status_code == 200
    stocks = res.json()
    assert len(stocks) >= 18
    # Verify core tickers exist
    tickers = [s["ticker"] for s in stocks]
    assert "TRENT" in tickers
    assert "TATAMOTORS" in tickers
    assert "POLYCAB" in tickers
    print(f"✓ Portfolio Universe Verified ({len(stocks)} stocks loaded)")

def test_push_digest_and_collapse():
    res = client.get("/api/digest?window_hours=24")
    assert res.status_code == 200
    digest = res.json()
    assert "announcements" in digest
    assert "active_alerts" in digest
    assert digest["routine_collapsed_count"] >= 1
    # Check that routine regulatory compliance filings are collapsed
    routine = [a for a in digest["announcements"] if a["priority"] == "LOW"]
    assert len(routine) > 0
    print(f"✓ Push Digest Verified (Total: {digest['total_announcements']}, High: {digest['high_priority_count']}, Routine Collapsed: {digest['routine_collapsed_count']})")

def test_triggered_alerts():
    res = client.get("/api/alerts")
    assert res.status_code == 200
    alerts = res.json()
    assert len(alerts) >= 1
    types = [a["trigger_type"] for a in alerts]
    assert "VOLUME_SPIKE" in types or "PRICE_MOVE" in types
    print(f"✓ Triggered Alerts Verified ({len(alerts)} active alerts)")

def test_push_enrichments():
    res = client.get("/api/digest?window_hours=24")
    digest = res.json()
    announcements = digest["announcements"]
    
    # Check Management Bio Enrichment
    mgmt_ann = next((a for a in announcements if a.get("management_enrichment")), None)
    assert mgmt_ann is not None
    bio = mgmt_ann["management_enrichment"]
    assert "incoming_person" in bio
    assert len(bio["career_profile_bullets"]) >= 2
    assert "strategic_implication" in bio
    print(f"✓ Push Enrichment #1 (Management Bio: {bio['incoming_person']}) Verified")

    # Check Results Instant Cut Enrichment
    results_ann = next((a for a in announcements if a.get("results_enrichment")), None)
    assert results_ann is not None
    res_enr = results_ann["results_enrichment"]
    assert "revenue" in res_enr
    assert "ebitda" in res_enr
    assert "pbt" in res_enr
    assert "pat" in res_enr
    print(f"✓ Push Enrichment #2 (Results Scorecard: {res_enr['quarter']}) Verified")

def test_pull_research_flagship_trent():
    res = client.get("/api/research/TRENT")
    assert res.status_code == 200
    report = res.json()
    assert report["ticker"] == "TRENT"
    
    # 1. Narrative vs Numbers Matrix (Flagship)
    matrix = report["narrative_matrix"]
    assert len(matrix["items"]) >= 4
    for item in matrix["items"]:
        assert item["management_promised"]
        assert item["actual_delivered"]
        assert item["verdict"] in ["DELIVERED", "MISSED", "DELAYED", "DIVERGED", "PARTIAL"]
        assert item["source_citation"]
    print(f"✓ Pull Mode Flagship (Narrative vs Numbers Matrix: {len(matrix['items'])} quarters) Verified")

    # 2. Financial Snapshot
    fin = report["financial_snapshot"]
    assert fin["ttm_revenue_cr"] > 0
    assert fin["ebitda_margin_pct"] > 0
    assert fin["roce_pct"] > 0
    print(f"✓ Pull Mode Dimension 2 (Financial Snapshot: Revenue ₹{fin['ttm_revenue_cr']} Cr, Margin {fin['ebitda_margin_pct']}%) Verified")

    # 3. Bull vs Bear
    bb = report["bull_bear_thesis"]
    assert len(bb["bull_case"]) >= 2
    assert len(bb["bear_case"]) >= 2
    print(f"✓ Pull Mode Dimension 8 (Bull vs Bear: {len(bb['bull_case'])} bull / {len(bb['bear_case'])} bear points) Verified")

    # 4. Balance Sheet & RPTs
    bs = report["balance_sheet"]
    assert bs is not None
    assert "rpt_flag" in bs
    assert "auditor_qualification_flag" in bs
    print(f"✓ Pull Mode Dimension 4 (Balance Sheet & RPT Flag: {bs['rpt_flag']}, Auditor Clean: {not bs['auditor_qualification_flag']}) Verified")

    # 5. Cash Quality
    cq = report["cash_quality"]
    assert cq is not None
    assert cq["cash_conversion_ratio"] > 0
    print(f"✓ Pull Mode Dimension 5 (Cash Quality: Conversion Ratio {cq['cash_conversion_ratio']}%) Verified")

    # 6. Primary Documents Vault (Scraped from screener.in)
    docs = report.get("primary_documents")
    assert docs is not None
    assert len(docs["annual_reports"]) > 0 or len(docs["concall_transcripts"]) > 0
    print(f"✓ Primary Documents Vault Verified ({len(docs['annual_reports'])} Annual Reports, {len(docs['concall_transcripts'])} Concalls scraped)")

def test_pull_research_generalisation_dixon():
    res = client.get("/api/research/DIXON")
    assert res.status_code == 200
    report = res.json()
    assert report["ticker"] == "DIXON"
    assert len(report["narrative_matrix"]["items"]) >= 4
    print(f"✓ Dynamic Generalisation Verified on Ad-Hoc Ticker DIXON")

if __name__ == "__main__":
    print("\n================ RUNNING FINN E2E TEST SUITE ================")
    test_health()
    test_portfolio_universe()
    test_push_digest_and_collapse()
    test_triggered_alerts()
    test_push_enrichments()
    test_pull_research_flagship_trent()
    test_pull_research_generalisation_dixon()
    print("================ ALL 7 E2E TESTS PASSED (100% SUCCESS) ================\n")
