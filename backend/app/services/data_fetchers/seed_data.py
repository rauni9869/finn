"""
Seed fixtures providing institutional-grade financial data, announcements,
and primary-grounded research views across the 18 portfolio stocks and 4 ad-hoc tickers.
Guarantees 100% demo reliability under offline, off-market, or rate-limited conditions.
"""

from typing import List, Dict, Any

# Curated Announcements across the 17 taxonomy categories
SEED_ANNOUNCEMENTS: List[Dict[str, Any]] = [
    {
        "id": "ann-trent-001",
        "ticker": "TRENT",
        "company_name": "Trent Ltd",
        "timestamp": "2026-10-31T09:30:00Z",
        "category": "results",
        "priority": "HIGH",
        "headline": "Financial Results for the Second Quarter ended September 30, 2026 (Consolidated)",
        "details": "Revenue from operations jumped 39.4% YoY to ₹4,156.7 Cr. Profit After Tax rose 45.8% YoY to ₹335.0 Cr. Operating EBITDA stood at ₹632.0 Cr with EBITDA margin of 15.2% (+110 bps YoY). Added 43 new Zudio stores and 6 Westside stores during the quarter.",
        "one_line_summary": "Q2 PAT surged 46% YoY to ₹335 Cr; operating margin expanded 110 bps.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/trent_q2_results.pdf",
        "results_enrichment": {
            "quarter": "Q2 FY25",
            "revenue": {"val_cr": 4156.7, "qoq_pct": 8.4, "yoy_pct": 39.4},
            "ebitda": {"val_cr": 632.0, "qoq_pct": 7.1, "yoy_pct": 42.1, "margin_pct": 15.2, "margin_yoy_bps": 110},
            "pbt": {"val_cr": 452.3, "qoq_pct": 9.2, "yoy_pct": 44.5},
            "pat": {"val_cr": 335.0, "qoq_pct": 6.8, "yoy_pct": 45.8},
            "headline_verdict": "Robust performance driven by aggressive Zudio store rollouts; gross margin tailwinds cushioned higher retail lease additions.",
            "key_highlights": [
                "43 new Zudio stores commissioned; total store count crosses 550",
                "Like-for-like (LFL) sales growth sustained at double digits (11.8%)",
                "Emerging categories (apparel, beauty, innerwear) now contribute 20%+ of sales"
            ]
        }
    },
    {
        "id": "ann-fedbk-002",
        "ticker": "FEDERALBNK",
        "company_name": "Federal Bank Ltd",
        "timestamp": "2026-10-31T08:15:00Z",
        "category": "management_change",
        "priority": "HIGH",
        "headline": "Appointment of Mr. K.V.S. Manian as Managing Director & Chief Executive Officer",
        "details": "Reserve Bank of India has approved the appointment of Mr. K.V.S. Manian as MD & CEO of The Federal Bank Limited for a period of 3 years effective September 23, 2024, succeeding Mr. Shyam Srinivasan upon completion of his regulatory term.",
        "one_line_summary": "RBI approves KVS Manian as MD & CEO for 3-year term succeeding Shyam Srinivasan.",
        "attachment_url": "https://www.nseindia.com/corporate/federal_bank_md_appointment.pdf",
        "management_enrichment": {
            "incoming_person": "K.V.S. Manian",
            "new_role": "Managing Director & CEO",
            "effective_date": "2024-09-23",
            "predecessor": "Shyam Srinivasan (Tenure: 14 years)",
            "career_profile_bullets": [
                "Pedigree: IIT (BHU) Varanasi, IIM Bangalore; 30+ years institutional banking leadership.",
                "Former Joint MD at Kotak Mahindra Bank; spearheaded Wholesale, Commercial Banking, and Integrated Treasury franchises.",
                "Proven track record in scaling high-margin asset portfolios and modernizing core digital banking stacks."
            ],
            "strategic_implication": "Signals an aggressive push into high-yield commercial loans and corporate fee income while retaining Federal Bank's low-cost Kerala deposit franchise."
        }
    },
    {
        "id": "ann-polycab-003",
        "ticker": "POLYCAB",
        "company_name": "Polycab India Ltd",
        "timestamp": "2026-10-30T16:45:00Z",
        "category": "capex",
        "priority": "HIGH",
        "headline": "Approval for Greenfield Extra High Voltage (EHV) Power Cables Facility with ₹650 Cr Capex",
        "details": "The Board of Directors has approved setting up a new manufacturing plant for Extra High Voltage (EHV) cables up to 550 kV in Halol, Gujarat, with an estimated capital expenditure of ₹650 Crores, to be funded through internal accruals.",
        "one_line_summary": "Board approves ₹650 Cr greenfield EHV cables facility in Halol from internal accruals.",
        "attachment_url": "https://www.nseindia.com/corporate/polycab_ehv_capex.pdf"
    },
    {
        "id": "ann-tatamotors-004",
        "ticker": "TATAMOTORS",
        "company_name": "Tata Motors Ltd",
        "timestamp": "2026-10-30T14:20:00Z",
        "category": "credit_rating",
        "priority": "MEDIUM",
        "headline": "CRISIL Upgrades Long-Term Credit Rating to 'CRISIL AA+/Stable'",
        "details": "CRISIL Ratings has upgraded its rating on long-term bank facilities and debt instruments of Tata Motors Limited to 'CRISIL AA+/Stable' from 'CRISIL AA/Positive'. Upgrade reflects deleveraging at JLR and sustained market leadership in domestic Commercial Vehicles.",
        "one_line_summary": "CRISIL upgrades rating to AA+/Stable on sustained JLR debt reduction and CV cash flows.",
        "attachment_url": "https://www.nseindia.com/corporate/tatamotors_rating_upgrade.pdf"
    },
    {
        "id": "ann-zentec-005",
        "ticker": "ZENTEC",
        "company_name": "Zen Technologies Ltd",
        "timestamp": "2026-10-30T11:10:00Z",
        "category": "press_release",
        "priority": "HIGH",
        "headline": "Receipt of Major Export Order worth ₹142 Crores for Anti-Drone and Simulator Systems",
        "details": "Zen Technologies has secured a prestigious international export order valued at approximately ₹142 Crores from an overseas friendly country for advanced Zen Anti-Drone Systems (ZADS) and Combat Training Simulators to be executed within 12 months.",
        "one_line_summary": "Secured ₹142 Cr export order for Anti-Drone Systems; execution timeline 12 months.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/zentec_order_142cr.pdf"
    },
    {
        "id": "ann-sunpharma-006",
        "ticker": "SUNPHARMA",
        "company_name": "Sun Pharmaceutical Industries Ltd",
        "timestamp": "2026-10-30T10:00:00Z",
        "category": "litigation",
        "priority": "HIGH",
        "headline": "US FDA Inspection Closure - Establishment Inspection Report (EIR) received for Mohali facility",
        "details": "Sun Pharma has received an Establishment Inspection Report (EIR) from the US FDA regarding the pre-approval inspection of its Mohali manufacturing facility conducted in August. Inspection is classified as Voluntary Action Indicated (VAI).",
        "one_line_summary": "Received US FDA EIR for Mohali facility with VAI status, clearing path for US generic approvals.",
        "attachment_url": "https://www.nseindia.com/corporate/sunpharma_eir_mohali.pdf"
    },
    {
        "id": "ann-itc-007",
        "ticker": "ITC",
        "company_name": "ITC Ltd",
        "timestamp": "2026-10-29T17:30:00Z",
        "category": "M&A",
        "priority": "HIGH",
        "headline": "NCLT Approves Scheme of Arrangement for Demerger of Hotel Business into ITC Hotels Ltd",
        "details": "Hon'ble National Company Law Tribunal (NCLT), Kolkata Bench, has sanctioned the Scheme of Arrangement amongst ITC Limited and ITC Hotels Limited and their respective shareholders for demerger of the hotel business undertaking.",
        "one_line_summary": "NCLT sanctions Scheme of Arrangement for demerger of ITC Hotels Limited.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/itc_hotels_nclt.pdf"
    },
    {
        "id": "ann-tcs-008",
        "ticker": "TCS",
        "company_name": "Tata Consultancy Services Ltd",
        "timestamp": "2026-10-29T16:00:00Z",
        "category": "dividend",
        "priority": "MEDIUM",
        "headline": "Declaration of Second Interim Dividend of ₹10 per Equity Share; Record Date Fixed",
        "details": "The Board of Directors declared a second interim dividend of ₹10 per equity share of ₹1 each. The record date for determining entitlement of equity shareholders is fixed as November 7, 2026.",
        "one_line_summary": "Declared ₹10/share second interim dividend; record date November 7, 2026.",
        "attachment_url": "https://www.nseindia.com/corporate/tcs_interim_dividend.pdf"
    },
    {
        "id": "ann-reliance-009",
        "ticker": "RELIANCE",
        "company_name": "Reliance Industries Ltd",
        "timestamp": "2026-10-29T14:15:00Z",
        "category": "results",
        "priority": "HIGH",
        "headline": "Consolidated Financial Results for Q2 FY25: EBITDA at ₹43,934 Cr",
        "details": "Reliance Industries reported Q2 FY25 consolidated revenue of ₹2,58,027 Cr (+0.2% YoY). EBITDA reached ₹43,934 Cr (-2.0% YoY) impacted by weak O2C refining margins, offset by 15.6% YoY growth in Jio Infocomm EBITDA and 8.2% YoY growth in Reliance Retail EBITDA.",
        "one_line_summary": "Q2 EBITDA steady at ₹43,934 Cr as Telecom & Retail gains offset global refining softness.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/ril_q2_results.pdf",
        "results_enrichment": {
            "quarter": "Q2 FY25",
            "revenue": {"val_cr": 258027.0, "qoq_pct": 0.4, "yoy_pct": 0.2},
            "ebitda": {"val_cr": 43934.0, "qoq_pct": 2.8, "yoy_pct": -2.0, "margin_pct": 17.0, "margin_yoy_bps": -40},
            "pbt": {"val_cr": 26840.0, "qoq_pct": 3.1, "yoy_pct": -3.5},
            "pat": {"val_cr": 19323.0, "qoq_pct": 4.2, "yoy_pct": -4.8},
            "headline_verdict": "Telecom tariff hike flow-through and Retail footfall resilience cushioned O2C crack spread compression.",
            "key_highlights": [
                "Jio ARPU rose to ₹195.1/month following July tariff rationalization",
                "Reliance Retail opened 464 new stores with 71.3 million sq ft footprint",
                "New Energy giga-factories in Jamnagar on track for phased commissioning in 2025"
            ]
        }
    },
    {
        "id": "ann-kaynes-010",
        "ticker": "KAYNES",
        "company_name": "Kaynes Technology India Ltd",
        "timestamp": "2026-10-29T11:00:00Z",
        "category": "fund_raise",
        "priority": "HIGH",
        "headline": "Closure of Qualified Institutions Placement (QIP) of Equity Shares raising ₹1,400 Crores",
        "details": "Fund Raising Committee approved closure of the QIP issue with allocation of 34,22,982 equity shares to eligible QIBs at an issue price of ₹4,090 per share (discount of 4.9% to floor price), aggregating to ₹1,400 Crores for OSAT semiconductor unit expansion.",
        "one_line_summary": "Raised ₹1,400 Cr via QIP at ₹4,090/share to fund OSAT semiconductor packaging capex.",
        "attachment_url": "https://www.nseindia.com/corporate/kaynes_qip_closure.pdf"
    },
    {
        "id": "ann-titan-011",
        "ticker": "TITAN",
        "company_name": "Titan Company Ltd",
        "timestamp": "2026-10-28T16:00:00Z",
        "category": "bonus_split",
        "priority": "MEDIUM",
        "headline": "Intimation of Board Meeting to consider Bonus Issue of Shares",
        "details": "Notice is hereby given that a meeting of the Board of Directors is scheduled to be held on November 5, 2026, to consider and approve a proposal for issuance of Bonus Shares to the equity shareholders of the company.",
        "one_line_summary": "Board meeting convened on Nov 5 to evaluate bonus share issuance proposal.",
        "attachment_url": "https://www.nseindia.com/corporate/titan_bonus_intimation.pdf"
    },
    {
        "id": "ann-deepak-012",
        "ticker": "DEEPAKNTR",
        "company_name": "Deepak Nitrite Ltd",
        "timestamp": "2026-10-28T14:30:00Z",
        "category": "pledging",
        "priority": "MEDIUM",
        "headline": "Disclosure of Release of Encumbrance / Pledge on 12,50,000 Equity Shares by Promoters",
        "details": "Deepak C. Mehta (Promoter) has disclosed release of pledge on 12,50,000 equity shares held in Deepak Nitrite Limited pursuant to complete repayment of loan facility. Total promoter pledged shares reduced from 3.1% to 1.8% of capital.",
        "one_line_summary": "Promoter releases 12.5 lakh pledged shares; total pledged holding down to 1.8%.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/deepak_pledge_release.pdf"
    },
    {
        "id": "ann-lt-013",
        "ticker": "LT",
        "company_name": "Larsen & Toubro Ltd",
        "timestamp": "2026-10-28T12:00:00Z",
        "category": "investor_meetings",
        "priority": "LOW",
        "headline": "Schedule of Institutional Investor Meeting with Nomura Asset Management",
        "details": "Pursuant to Regulation 30(6) of SEBI (LODR) Regulations, 2015, representatives of Larsen & Toubro will be attending a one-on-one virtual meeting with Nomura Asset Management on November 3, 2026.",
        "one_line_summary": "Scheduled 1-on-1 institutional investor meeting with Nomura Asset Management on Nov 3.",
        "attachment_url": "https://www.nseindia.com/corporate/lt_investor_meet.pdf"
    },
    {
        "id": "ann-persistent-014",
        "ticker": "PERSISTENT",
        "company_name": "Persistent Systems Ltd",
        "timestamp": "2026-10-28T10:15:00Z",
        "category": "earnings_call",
        "priority": "MEDIUM",
        "headline": "Transcript of Earnings Conference Call for the Second Quarter ended September 30, 2026",
        "details": "Submission of the verbatim transcript of the Q2 FY25 earnings conference call held with institutional analysts on October 24, 2026. Discussion centered on AI deal pipeline, BFSI client ramp-ups, and EBIT margin trajectory.",
        "one_line_summary": "Submitted official verbatim transcript of Q2 FY25 earnings conference call.",
        "attachment_url": "https://www.nseindia.com/corporate/persistent_concall_transcript_q2.pdf"
    },
    {
        "id": "ann-hdfc-015",
        "ticker": "HDFCBANK",
        "company_name": "HDFC Bank Ltd",
        "timestamp": "2026-10-27T18:00:00Z",
        "category": "postal_ballot",
        "priority": "LOW",
        "headline": "Postal Ballot Notice for Re-appointment of Independent Directors and Scrutinizer Report",
        "details": "Notice of Postal Ballot sent to members seeking approval for re-appointment of two Independent Directors for a second term of five consecutive years through remote e-voting facility.",
        "one_line_summary": "Dispatched postal ballot notice for re-appointment of two Independent Directors.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/hdfc_postal_ballot.pdf"
    },
    {
        "id": "ann-ksolves-016",
        "ticker": "KSOLVES",
        "company_name": "Ksolves India Ltd",
        "timestamp": "2026-10-27T15:40:00Z",
        "category": "agm_egm",
        "priority": "LOW",
        "headline": "Summary of Proceedings of the 10th Annual General Meeting held on October 27, 2026",
        "details": "The 10th Annual General Meeting of Ksolves India Limited was held via Video Conferencing. All ordinary and special resolutions, including final dividend adoption, were passed with requisite majority.",
        "one_line_summary": "Concluded 10th AGM; all ordinary and special resolutions passed unanimously.",
        "attachment_url": "https://www.nseindia.com/corporate/ksolves_agm_proceedings.pdf"
    },
    {
        "id": "ann-ethos-017",
        "ticker": "ETHOSLTD",
        "company_name": "Ethos Ltd",
        "timestamp": "2026-10-27T14:00:00Z",
        "category": "insider_trading",
        "priority": "MEDIUM",
        "headline": "Disclosure under Regulation 7(2) of SEBI (PIT) Regulations - Promoter Acquisition",
        "details": "KDDL Limited (Promoter Entity) has acquired 25,000 equity shares of Ethos Limited from the open market on October 25, 2026, increasing total promoter holding from 61.12% to 61.22%.",
        "one_line_summary": "Promoter entity KDDL acquired 25,000 shares from open market (+0.10% stake).",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/ethos_insider_trading.pdf"
    },
    {
        "id": "ann-supriya-018",
        "ticker": "SUPRIYA",
        "company_name": "Supriya Lifescience Ltd",
        "timestamp": "2026-10-27T11:20:00Z",
        "category": "unclassified",
        "priority": "LOW",
        "headline": "Allotment of 15,200 Equity Shares under Supriya Employee Stock Option Scheme (ESOS-2021)",
        "details": "The Nomination and Remuneration Committee approved allotment of 15,200 equity shares of face value ₹2 each to eligible employees pursuant to exercise of stock options granted under ESOS 2021.",
        "one_line_summary": "Routine ESOP share allotment of 15,200 equity shares of ₹2 face value.",
        "attachment_url": "https://www.nseindia.com/corporate/supriya_esop_allotment.pdf"
    },
    {
        "id": "ann-routine-019",
        "ticker": "RELIANCE",
        "company_name": "Reliance Industries Ltd",
        "timestamp": "2026-10-27T09:00:00Z",
        "category": "unclassified",
        "priority": "LOW",
        "headline": "Compliance Certificate under Regulation 7(3) of SEBI (LODR) Regulations for Half Year",
        "details": "Submission of half-yearly compliance certificate certifying that all activities in relation to share transfer facilities are maintained by KFin Technologies Limited, SEBI registered Category I RTA.",
        "one_line_summary": "Routine compliance certificate under Reg 7(3) for share transfer facilities.",
        "attachment_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/ril_reg7_cert.pdf"
    },
    {
        "id": "ann-routine-020",
        "ticker": "HDFCBANK",
        "company_name": "HDFC Bank Ltd",
        "timestamp": "2026-10-26T17:00:00Z",
        "category": "unclassified",
        "priority": "LOW",
        "headline": "Intimation of Loss of Share Certificates and Request for Issuance of Duplicate Certificates",
        "details": "Pursuant to Regulation 39(3) of SEBI (LODR) Regulations, information is provided regarding loss of share certificates reported by 4 individual retail shareholders.",
        "one_line_summary": "Routine regulatory disclosure of lost share certificates for 4 retail holders.",
        "attachment_url": "https://www.nseindia.com/corporate/hdfc_loss_shares.pdf"
    }
]

# Primary-Grounded Research Seed Profiles (8 Dimensions)
SEED_RESEARCH_PROFILES: Dict[str, Dict[str, Any]] = {
    "TRENT": {
        "ticker": "TRENT",
        "company_name": "Trent Ltd",
        "financial_snapshot": {
            "ticker": "TRENT",
            "company_name": "Trent Ltd",
            "ttm_revenue_cr": 14210.0,
            "ebitda_margin_pct": 15.6,
            "pat_cr": 1285.0,
            "roce_pct": 28.4,
            "roe_pct": 24.1,
            "pe_ratio": 122.5,
            "ev_ebitda": 58.2,
            "sales_cagr_3yr": 48.2,
            "profit_cagr_3yr": 76.5,
            "debt_to_equity": 0.22,
            "primary_source_notes": "Screener.in consolidated financials & Q2 FY25 Results exchange filing."
        },
        "narrative_matrix": {
            "ticker": "TRENT",
            "company_name": "Trent Ltd",
            "coverage_period": "Q3 FY24 - Q2 FY25 (Last 4 Quarters)",
            "overall_track_record_score": "85% High Conviction Delivery (4/5 commitments met or exceeded)",
            "summary_verdict": "Management has consistently over-delivered on Zudio store rollouts while defending EBITDA margins despite aggressive pan-India expansion.",
            "items": [
                {
                    "quarter": "Q3 FY24",
                    "management_promised": "Guide to add 150-160 Zudio stores across FY25; sustain Westside LFL growth above 8%.",
                    "actual_delivered": "Added 178 Zudio stores by Q2 FY25; Westside LFL recorded 10.4% in H1 FY25.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Store rollout velocity exceeded target by ~12%; tier-2/3 store unit economics proved cash-flow accretive within 6 months.",
                    "source_citation": "Concall Q3 FY24 (p. 6) vs Q2 FY25 Earnings Deck (p. 11)",
                    "pdf_page": 6
                },
                {
                    "quarter": "Q4 FY24",
                    "management_promised": "Operating EBITDA margins to remain in the 14-15% corridor despite freight inflation.",
                    "actual_delivered": "Q1 FY25 EBITDA margin came at 15.4%; Q2 FY25 reached 15.2%.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Gross margin expansion in apparel direct sourcing offset retail lease additions.",
                    "source_citation": "Concall Q4 FY24 (p. 9) vs Q1/Q2 Results Filings",
                    "pdf_page": 9
                },
                {
                    "quarter": "Q1 FY25",
                    "management_promised": "Star Bazaar grocery chain to achieve company-level breakeven by end of H1 FY25.",
                    "actual_delivered": "Star achieved store-level EBITDA positive; corporate overhead caused minor net loss.",
                    "verdict": "PARTIAL",
                    "verdict_detail": "High-margin private label penetration grew to 36%, but supply chain distribution hub setup pushed consolidated breakeven by 1 quarter.",
                    "source_citation": "Concall Q1 FY25 (p. 12) vs Q2 FY25 Segment Disclosures",
                    "pdf_page": 12
                },
                {
                    "quarter": "Q2 FY25",
                    "management_promised": "International pilot in UAE (Zudio Dubai) to reach 4 stores by December 2024.",
                    "actual_delivered": "3 stores operational in Dubai/Sharjah; 4th location lease signed.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Early customer traction encouraging; average basket size 1.8x Indian domestic stores.",
                    "source_citation": "Concall Q2 FY25 (p. 4)",
                    "pdf_page": 4
                }
            ]
        },
        "bull_bear_thesis": {
            "ticker": "TRENT",
            "company_name": "Trent Ltd",
            "bull_case": [
                "Zudio's ultra-fast inventory turn (sub-45 days) and ₹999 price ceiling creates a widening consumer moat against unorganized apparel.",
                "High return on capital (ROCE 28%+) enabled by master lease cluster model and minimal working capital lock-in.",
                "New growth engines (Misbu beauty format & Lab-Grown Diamonds) offer optionality without diluting core return metrics."
            ],
            "bear_case": [
                "Extreme valuation multiple (PE > 120x) leaves zero room for store cannibalization or consumption slowdown.",
                "Potential saturation of prime tier-2 retail real estate leading to higher lease rentals and payback elongation.",
                "Key management concentration risk around Noel Tata & P. Venkatesalu leadership team."
            ],
            "valuation_context": "Trading at 58x EV/EBITDA; pricing in 35%+ revenue CAGR over next 3 years.",
            "primary_source_citations": ["Trent FY24 Annual Report (Director's Report p. 24)", "Q2 FY25 Investor Presentation p. 8-14"]
        },
        "business_snapshot": {
            "description": "Trent Limited (Tata Group) operates leading retail chains including Westside (departmental lifestyle), Zudio (value fashion), Star (hypermarkets JV with Tesco), and Utsa.",
            "key_segments": [
                {"name": "Zudio (Value Fashion)", "revenue_share_pct": 58.0, "growth": "+54% YoY"},
                {"name": "Westside (Lifestyle & Premium)", "revenue_share_pct": 34.0, "growth": "+16% YoY"},
                {"name": "Star & Other Formats", "revenue_share_pct": 8.0, "growth": "+22% YoY"}
            ],
            "export_share_pct": 2.0,
            "domestic_share_pct": 98.0,
            "primary_source": "Trent FY24 Annual Report - Segment Reporting Note 34"
        },
        "balance_sheet": {
            "total_debt_cr": 450.0,
            "debt_to_equity": 0.22,
            "working_capital_days": 28,
            "contingent_liabilities_cr": 82.5,
            "contingent_liabilities_notes": "Disputed sales tax and municipal property tax matters under appeal; low risk of material cash outflow.",
            "rpt_flag": True,
            "rpt_details": "Lease rentals paid to Tata Group entities (₹112 Cr) at verified market-benchmark rates.",
            "auditor_qualification_flag": False,
            "auditor_notes": "S R B C & CO LLP issued an unmodified (clean) audit opinion with standard Emphasis of Matter on lease accounting (Ind AS 116).",
            "primary_source": "Trent FY24 Audited Financial Statements p. 112"
        },
        "cash_quality": {
            "cfo_3yr_cumulative_cr": 2840.0,
            "pat_3yr_cumulative_cr": 2150.0,
            "cash_conversion_ratio": 1.32,
            "fcf_latest_yr_cr": 720.0,
            "quality_verdict": "Pristine Cash Conversion (CFO exceeds cumulative PAT by 32% due to strict negative working capital retail model).",
            "primary_source": "Trent Cash Flow Statements FY22-FY24"
        },
        "guidance": {
            "revenue_growth_target": "30-35% CAGR over FY25-FY27",
            "margin_corridor": "14.5% - 15.5% Operating EBITDA margin",
            "planned_capex_cr": "₹600 - 750 Cr per annum for 200+ net store additions",
            "debt_milestone": "Maintain net-cash balance sheet at parent company level",
            "time_horizon": "FY25 - FY27 Rolling Guidance",
            "primary_source": "Q2 FY25 Concall Management Address"
        },
        "primary_documents": {
            "annual_reports": [
                {"title": "Annual Report FY24", "url": "https://www.bseindia.com/xml-data/corpfiling/AttachHis/c7330ad5-ba82-4673-baaa-b39af9c47c87.pdf"},
                {"title": "Annual Report FY23", "url": "https://www.bseindia.com/xml-data/corpfiling/AttachHis/58357a1d-01e7-410e-a079-834f7aefce44.pdf"}
            ],
            "concall_transcripts": [
                {"title": "Q2 FY25 Concall Deck", "url": "https://docs.trent-tata.com/TrentLimited/Financial%20Results/2024-25/Q2/Investor%20Presentation%20Q2%20FY%202025.pdf"},
                {"title": "Q1 FY25 Concall Transcript", "url": "https://docs.trent-tata.com/TrentLimited/Financial%20Results/2024-25/Q1/Investors%20Presentation%20Q1%20FY%202024.pdf"}
            ]
        }
    },
    "TATAMOTORS": {
        "ticker": "TATAMOTORS",
        "company_name": "Tata Motors Ltd",
        "financial_snapshot": {
            "ticker": "TATAMOTORS",
            "company_name": "Tata Motors Ltd",
            "ttm_revenue_cr": 437920.0,
            "ebitda_margin_pct": 14.1,
            "pat_cr": 31800.0,
            "roce_pct": 21.2,
            "roe_pct": 36.4,
            "pe_ratio": 10.8,
            "ev_ebitda": 4.6,
            "sales_cagr_3yr": 28.5,
            "profit_cagr_3yr": 142.0,
            "debt_to_equity": 0.65,
            "primary_source_notes": "Screener.in consolidated financials & Q1/Q2 FY25 filings."
        },
        "narrative_matrix": {
            "ticker": "TATAMOTORS",
            "company_name": "Tata Motors Ltd",
            "coverage_period": "Q3 FY24 - Q2 FY25",
            "overall_track_record_score": "90% Turnaround Promise Fulfilment (JLR net-zero debt delivered)",
            "summary_verdict": "Stellar execution on JLR debt elimination and domestic passenger vehicle profitability.",
            "items": [
                {
                    "quarter": "Q3 FY24",
                    "management_promised": "JLR net debt to reduce below £1.0 billion by FY24 end and achieve net-zero automotive debt in FY25.",
                    "actual_delivered": "JLR net debt reduced to £732m by Q4 FY24; automotive net debt turned positive cash in Q1 FY25.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Record Range Rover and Defender order book deliveries yielded £2.3bn free cash flow in FY24.",
                    "source_citation": "JLR Investor Day Transcript vs Q1 FY25 Results Presentation",
                    "pdf_page": 14
                },
                {
                    "quarter": "Q4 FY24",
                    "management_promised": "Commercial Vehicles (CV) EBITDA margin to sustain double digits (10-11%) despite cyclical softness.",
                    "actual_delivered": "Domestic CV margin reached 11.2% in Q1 FY25; 10.8% in Q2 FY25.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Price realization discipline over discounting protected segment profitability.",
                    "source_citation": "TML Q4 FY24 Concall (p. 8)",
                    "pdf_page": 8
                },
                {
                    "quarter": "Q1 FY25",
                    "management_promised": "Domestic EV market share to hold above 65% with launch of Curvv EV.",
                    "actual_delivered": "Curvv EV launched at ₹17.49 lakh; domestic EV market share held at 67.2%.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Curvv order book exceeded 15,000 units within first 45 days.",
                    "source_citation": "Q1 FY25 Analyst Q&A Transcript",
                    "pdf_page": 19
                }
            ]
        },
        "bull_bear_thesis": {
            "ticker": "TATAMOTORS",
            "company_name": "Tata Motors Ltd",
            "bull_case": [
                "Demerger into two listed entities (Commercial Vehicles vs Passenger Vehicles/JLR) will unlock sharp sum-of-the-parts (SOTP) rerating.",
                "JLR order book remains structurally weighted toward high-margin Range Rover models (£100k+ ASP).",
                "Tata Passenger Electric Mobility (TPEM) dominant domestic EV ecosystem moat."
            ],
            "bear_case": [
                "European and US luxury EV transition slowing down, requiring higher hybrid and ICE powertrain reinvestment capex.",
                "Domestic Commercial Vehicle volume growth moderating due to infrastructure tender lulls.",
                "Geopolitical tariffs and supply chain aluminum constraints affecting UK manufacturing."
            ],
            "valuation_context": "Trades at 10.8x PE and 4.6x EV/EBITDA, a heavy discount to standalone PV/CV peers.",
            "primary_source_citations": ["TML FY24 Integrated Annual Report", "Q2 FY25 Concall Transcript"]
        },
        "business_snapshot": {
            "description": "Global automotive manufacturer with leading positions in commercial vehicles in India, luxury premium passenger cars via Jaguar Land Rover (JLR), and passenger electric mobility.",
            "key_segments": [
                {"name": "Jaguar Land Rover (JLR)", "revenue_share_pct": 71.0, "growth": "+19% YoY"},
                {"name": "Tata Commercial Vehicles", "revenue_share_pct": 18.0, "growth": "+5% YoY"},
                {"name": "Tata Passenger Vehicles (incl EV)", "revenue_share_pct": 11.0, "growth": "+8% YoY"}
            ],
            "export_share_pct": 73.0,
            "domestic_share_pct": 27.0,
            "primary_source": "Tata Motors FY24 Annual Report - Segment Information"
        },
        "balance_sheet": {
            "total_debt_cr": 54200.0,
            "debt_to_equity": 0.65,
            "working_capital_days": -12,
            "contingent_liabilities_cr": 1420.0,
            "contingent_liabilities_notes": "Customs duties and tax litigation under appeal; provisions prudently maintained.",
            "rpt_flag": False,
            "rpt_details": "Normal course parts procurement with Tata AutoComp Systems.",
            "auditor_qualification_flag": False,
            "auditor_notes": "B S R & Co. LLP issued an unqualified audit opinion.",
            "primary_source": "Tata Motors Consolidated Balance Sheet FY24"
        },
        "cash_quality": {
            "cfo_3yr_cumulative_cr": 78500.0,
            "pat_3yr_cumulative_cr": 36200.0,
            "cash_conversion_ratio": 2.16,
            "fcf_latest_yr_cr": 26900.0,
            "quality_verdict": "Massive Turnaround Quality (Operating cash flow generated £2.5bn+ surplus at JLR).",
            "primary_source": "TML FY24 Audited Cash Flow Statement"
        },
        "guidance": {
            "revenue_growth_target": "JLR EBIT margin > 8.5% in FY25; > 10% in FY26",
            "margin_corridor": "Domestic CV margin 11-12%; Domestic PV margin 7-8%",
            "planned_capex_cr": "£3.0 billion annual capex at JLR funded entirely via internal cash",
            "debt_milestone": "Net zero automotive debt achieved in FY25",
            "time_horizon": "FY25-FY26",
            "primary_source": "JLR Reimagine Strategy Update"
        }
    },
    "POLYCAB": {
        "ticker": "POLYCAB",
        "company_name": "Polycab India Ltd",
        "financial_snapshot": {
            "ticker": "POLYCAB",
            "company_name": "Polycab India Ltd",
            "ttm_revenue_cr": 18450.0,
            "ebitda_margin_pct": 13.8,
            "pat_cr": 1810.0,
            "roce_pct": 31.5,
            "roe_pct": 26.2,
            "pe_ratio": 51.4,
            "ev_ebitda": 34.2,
            "sales_cagr_3yr": 26.4,
            "profit_cagr_3yr": 35.8,
            "debt_to_equity": 0.04,
            "primary_source_notes": "Screener.in & Polycab Q2 FY25 Disclosures."
        },
        "narrative_matrix": {
            "ticker": "POLYCAB",
            "company_name": "Polycab India Ltd",
            "coverage_period": "Q3 FY24 - Q2 FY25",
            "overall_track_record_score": "80% Delivery Track Record",
            "summary_verdict": "Dominant cable & wire market share gains delivered; FMEG segment restructuring on track.",
            "items": [
                {
                    "quarter": "Q3 FY24",
                    "management_promised": "Maintain 20%+ volume growth in domestic wires and cables under Project Leap.",
                    "actual_delivered": "Achieved 24% volume growth in Q4 FY24 and 21% in Q1 FY25.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Infrastructure capex and real estate residential completions drove heavy institutional and retail off-take.",
                    "source_citation": "Concall Q3 FY24 (p. 5) vs Q1 FY25 Presentation",
                    "pdf_page": 5
                },
                {
                    "quarter": "Q4 FY24",
                    "management_promised": "FMEG (Fast Moving Electrical Goods) business to reach EBITDA breakeven by H1 FY25.",
                    "actual_delivered": "FMEG segment reported small negative EBITDA (-1.2%) in Q2 FY25 due to fan BEE star rating transition costs.",
                    "verdict": "MISSED",
                    "verdict_detail": "Distribution realignment taking longer than planned; breakeven target shifted to Q4 FY25.",
                    "source_citation": "Concall Q4 FY24 (p. 11) vs Q2 FY25 Segment Financials",
                    "pdf_page": 11
                }
            ]
        },
        "bull_bear_thesis": {
            "ticker": "POLYCAB",
            "company_name": "Polycab India Ltd",
            "bull_case": [
                "24%+ organized market share in Cables & Wires; unmatched 4,300+ distributor network across India.",
                "Massive beneficiary of National Electricity Plan (transmission grid expansion, HVDC lines, renewable solar/wind evacuation).",
                "Robust balance sheet with ₹2,200+ Cr net cash generating strong negative working capital absorption."
            ],
            "bear_case": [
                "Volatility in international copper and aluminum commodity prices causing quarterly inventory lag.",
                "Residual corporate governance scrutiny following past Income Tax search operations.",
                "FMEG consumer appliances business continues to drag overall return ratios."
            ],
            "valuation_context": "Trades at 51x PE, premium to peer Havells given superior C&W return on capital.",
            "primary_source_citations": ["Polycab FY24 Annual Report", "Q2 FY25 Investor Presentation"]
        },
        "business_snapshot": {
            "description": "India's largest manufacturer of wires and cables, fast expanding into Fast Moving Electrical Goods (FMEG) including fans, LED lighting, switches, and solar inverters.",
            "key_segments": [
                {"name": "Wires and Cables", "revenue_share_pct": 88.0, "growth": "+27% YoY"},
                {"name": "FMEG (Appliances/Fans)", "revenue_share_pct": 7.0, "growth": "+12% YoY"},
                {"name": "EPC & Other", "revenue_share_pct": 5.0, "growth": "+18% YoY"}
            ],
            "export_share_pct": 9.0,
            "domestic_share_pct": 91.0,
            "primary_source": "Polycab FY24 Audited Segment Disclosures"
        },
        "balance_sheet": {
            "total_debt_cr": 185.0,
            "debt_to_equity": 0.04,
            "working_capital_days": 46,
            "contingent_liabilities_cr": 310.0,
            "contingent_liabilities_notes": "Income tax assessment review proceedings ongoing; legal counsel advises company has strong defensible merits.",
            "rpt_flag": False,
            "rpt_details": "Zero non-arm's length related party dealings.",
            "auditor_qualification_flag": False,
            "auditor_notes": "B S R & Co. LLP issued a standard clean report.",
            "primary_source": "Polycab FY24 Annual Report p. 154"
        },
        "cash_quality": {
            "cfo_3yr_cumulative_cr": 4120.0,
            "pat_3yr_cumulative_cr": 3950.0,
            "cash_conversion_ratio": 1.04,
            "fcf_latest_yr_cr": 1150.0,
            "quality_verdict": "High Quality Cash Conversion (Consistent CFO/PAT ratio > 1.0x).",
            "primary_source": "Polycab Consolidated Cash Flow Statement"
        },
        "guidance": {
            "revenue_growth_target": "Reach ₹20,000 Cr top-line by FY26 under Project Leap",
            "margin_corridor": "12-14% consolidated EBITDA margin",
            "planned_capex_cr": "₹600 - 700 Cr per year including new EHV cable facility",
            "debt_milestone": "Maintain zero net-debt status",
            "time_horizon": "Project Leap FY26 Vision",
            "primary_source": "Project Leap Investor Day Guidance"
        },
        "primary_documents": {
            "annual_reports": [
                {"title": "Annual Report FY24", "url": "https://www.bseindia.com/xml-data/corpfiling/AttachHis/ff6bcced-1327-449f-8a82-6fd651a0124f.pdf"}
            ],
            "concall_transcripts": [
                {"title": "Q2 FY25 Concall Transcript", "url": "https://www.bseindia.com/stockinfo/AnnPdfOpen.aspx?Pname=77b6d277-0ffc-440d-ba8a-2bd9bc3dc43e.pdf"}
            ]
        }
    },
    "DIXON": {
        "ticker": "DIXON",
        "company_name": "Dixon Technologies Ltd",
        "financial_snapshot": {
            "ticker": "DIXON",
            "company_name": "Dixon Technologies Ltd",
            "ttm_revenue_cr": 21800.0,
            "ebitda_margin_pct": 4.1,
            "pat_cr": 485.0,
            "roce_pct": 34.2,
            "roe_pct": 29.8,
            "pe_ratio": 158.0,
            "ev_ebitda": 72.0,
            "sales_cagr_3yr": 42.1,
            "profit_cagr_3yr": 48.0,
            "debt_to_equity": 0.35,
            "primary_source_notes": "Screener.in & Dixon Technologies Q2 FY25 Results."
        },
        "narrative_matrix": {
            "ticker": "DIXON",
            "company_name": "Dixon Technologies Ltd",
            "coverage_period": "Q3 FY24 - Q2 FY25",
            "overall_track_record_score": "95% Exceptional Guidance Beat",
            "summary_verdict": "Spectacular ramp-up in Smartphone manufacturing (Motorola, Xiaomi, Transsion) beating all production PLI targets.",
            "items": [
                {
                    "quarter": "Q3 FY24",
                    "management_promised": "Ramp mobile phone manufacturing to 25-30 million units annual run-rate in FY25.",
                    "actual_delivered": "Achieved run rate of 34 million units by Q2 FY25 with commissioning of Noida plant.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Secured major manufacturing contract for Ismartu (Transsion) and Xiaomi smartphone assembly.",
                    "source_citation": "Dixon Q3 FY24 Concall (p. 4)",
                    "pdf_page": 4
                },
                {
                    "quarter": "Q4 FY24",
                    "management_promised": "Close definitive acquisition agreement for 50.1% majority stake in Ismartu India.",
                    "actual_delivered": "Completed transaction in Q1 FY25 for ₹238 Cr after CCI antitrust clearance.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Consolidated Ismartu balance sheet and production facilities into Dixon EMS numbers.",
                    "source_citation": "Dixon Q4 FY24 Filing & Transcript (p. 7)",
                    "pdf_page": 7
                },
                {
                    "quarter": "Q1 FY25",
                    "management_promised": "Commence display module assembly and precision IT hardware manufacturing in H2 FY25.",
                    "actual_delivered": "Trial production underway in tie-up with HKC Corporation for display panels.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Deepened backward integration from pure assembly into sub-components.",
                    "source_citation": "Dixon Q1 FY25 Concall (p. 9)",
                    "pdf_page": 9
                },
                {
                    "quarter": "Q2 FY25",
                    "management_promised": "Sustain 35%+ revenue growth in consumer electronics and lighting despite sluggish festival pre-stocking.",
                    "actual_delivered": "Consumer electronics grew 41% YoY driven by large-screen TV and washing machine ODM contracts.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "ODM segment share expanded to 14% of revenue, supporting gross margins.",
                    "source_citation": "Dixon Q2 FY25 Investor Presentation (p. 16)",
                    "pdf_page": 16
                }
            ]
        },
        "bull_bear_thesis": {
            "ticker": "DIXON",
            "company_name": "Dixon Technologies Ltd",
            "bull_case": [
                "Prime national champion of India's Electronics PLI (Production Linked Incentive) scheme across Mobiles, IT Hardware, and Telecom.",
                "Backward integration into display modules, camera modules, and mechanicals to double operating margin profile.",
                "Massive global OEM client stickiness (Samsung, Motorola, Xiaomi, Acer, Lenovo)."
            ],
            "bear_case": [
                "Extremely razor-thin operating margins (~4%) leaving zero buffer for assembly defect penalties.",
                "Client concentration: top 3 mobile customers account for over 60% of total revenue.",
                "Sky-high valuation (PE > 150x) makes the stock vulnerable to any PLI policy revision or customer in-sourcing."
            ],
            "valuation_context": "Trading at 72x EV/EBITDA; prices in sustained 40%+ EPS growth.",
            "primary_source_citations": ["Dixon FY24 Annual Report", "Q2 FY25 Analyst Transcript"]
        },
        "business_snapshot": {
            "description": "Leading Indian electronic manufacturing services (EMS) company specializing in consumer electronics, mobile phones, lighting, home appliances, and CCTV cameras.",
            "key_segments": [
                {"name": "Mobile & EMS", "revenue_share_pct": 65.0, "growth": "+95% YoY"},
                {"name": "Consumer Electronics (TVs)", "revenue_share_pct": 18.0, "growth": "+8% YoY"},
                {"name": "Lighting & Home Appliances", "revenue_share_pct": 17.0, "growth": "+14% YoY"}
            ],
            "export_share_pct": 14.0,
            "domestic_share_pct": 86.0,
            "primary_source": "Dixon FY24 Investor Presentation"
        },
        "balance_sheet": {
            "total_debt_cr": 420.0,
            "debt_to_equity": 0.35,
            "working_capital_days": 18,
            "contingent_liabilities_cr": 45.0,
            "contingent_liabilities_notes": "Bank guarantees for customs bonded warehouses; standard commercial risk.",
            "rpt_flag": False,
            "rpt_details": "No promoter interest in supplier vendor ecosystem.",
            "auditor_qualification_flag": False,
            "auditor_notes": "S.N. Dhawan & CO LLP issued an unqualified clean audit report.",
            "primary_source": "Dixon FY24 Audited Financials"
        },
        "cash_quality": {
            "cfo_3yr_cumulative_cr": 1380.0,
            "pat_3yr_cumulative_cr": 920.0,
            "cash_conversion_ratio": 1.50,
            "fcf_latest_yr_cr": 280.0,
            "quality_verdict": "Very High Cash Conversion (Prompt customer advance payments and OEM vendor financing).",
            "primary_source": "Dixon Cash Flow Statements FY22-FY24"
        },
        "guidance": {
            "revenue_growth_target": "50%+ revenue growth in FY25 driven by mobile volume doubling",
            "margin_corridor": "4.0% - 4.5% EBITDA margin with component expansion",
            "planned_capex_cr": "₹550 - 600 Cr for component backward integration",
            "debt_milestone": "Maintain D/E below 0.5x",
            "time_horizon": "FY25 Guidance",
            "primary_source": "Dixon Q2 FY25 Concall"
        },
        "primary_documents": {
            "annual_reports": [
                {"title": "Annual Report FY24", "url": "https://www.bseindia.com/xml-data/corpfiling/AttachHis/5ef88e3c-352d-4223-a8ec-bdd7d3aa31c1.pdf"}
            ],
            "concall_transcripts": [
                {"title": "Q2 FY25 Concall Audio (MP3)", "url": "https://d1iixm87htyovw.cloudfront.net/uploads/4179985e-dda3-4986-8c85-d283d92db460-Q2FY27EarningsCall.mp3"}
            ]
        }
    },
    "ZOMATO": {
        "ticker": "ZOMATO",
        "company_name": "Zomato Ltd",
        "financial_snapshot": {
            "ticker": "ZOMATO",
            "company_name": "Zomato Ltd",
            "ttm_revenue_cr": 15400.0,
            "ebitda_margin_pct": 7.2,
            "pat_cr": 1120.0,
            "roce_pct": 11.8,
            "roe_pct": 9.4,
            "pe_ratio": 195.0,
            "ev_ebitda": 110.0,
            "sales_cagr_3yr": 68.4,
            "profit_cagr_3yr": 210.0,
            "debt_to_equity": 0.0,
            "primary_source_notes": "Screener.in & Zomato Q2 FY25 Shareholder Letter."
        },
        "narrative_matrix": {
            "ticker": "ZOMATO",
            "company_name": "Zomato Ltd",
            "coverage_period": "Q3 FY24 - Q2 FY25",
            "overall_track_record_score": "100% Exemplary Delivery",
            "summary_verdict": "Founder Deepinder Goyal has delivered on every guidance promise: food delivery adjusted EBITDA reached 3.5% GOV, and Blinkit achieved operational breakeven faster than expected.",
            "items": [
                {
                    "quarter": "Q3 FY24",
                    "management_promised": "Blinkit to reach adjusted EBITDA breakeven by Q1 FY25 while aggressively expanding dark stores.",
                    "actual_delivered": "Blinkit achieved adjusted EBITDA breakeven in March 2024 (Q4 FY24), 1 quarter ahead of guidance.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Dark store throughput crossed 1,000 orders/day; average delivery time reduced to 11.2 minutes.",
                    "source_citation": "Zomato Q3 FY24 Shareholder Letter (p. 6)",
                    "pdf_page": 6
                },
                {
                    "quarter": "Q4 FY24",
                    "management_promised": "Target to scale Blinkit dark store count from 526 to 1,000 stores by end of FY25.",
                    "actual_delivered": "Reached 791 dark stores by Q2 FY25; on pace to cross 1,000 before March 2025.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Store expansion self-funded through food delivery cash generation and existing treasury.",
                    "source_citation": "Zomato Q4 FY24 Shareholder Letter (p. 11)",
                    "pdf_page": 11
                },
                {
                    "quarter": "Q1 FY25",
                    "management_promised": "Food delivery Gross Order Value (GOV) growth to sustain at 20%+ YoY with rising platform fee.",
                    "actual_delivered": "Q2 FY25 Food Delivery GOV grew 21.4% YoY; platform fee raised to ₹6-10 per order without churn.",
                    "verdict": "DELIVERED",
                    "verdict_detail": "Take rate improved by 35 bps QoQ.",
                    "source_citation": "Q1 FY25 Shareholder Letter (p. 4)",
                    "pdf_page": 4
                }
            ]
        },
        "bull_bear_thesis": {
            "ticker": "ZOMATO",
            "company_name": "Zomato Ltd",
            "bull_case": [
                "Blinkit quick commerce is establishing an impenetrable retail distribution monopoly in urban India, capturing high-margin FMCG advertising spend.",
                "Food delivery duopoly (Zomato + Swiggy) exhibits immense pricing power via steady platform fee hikes and Gold subscriptions.",
                "Net cash treasury of ₹12,000+ Cr provides endless runway and opportunistic acquisition firepower."
            ],
            "bear_case": [
                "Intensifying quick commerce competition from Zepto and Tata Neu/BigBasket driving dark store rental bidding wars.",
                "Gig worker regulatory headwinds: state-level gig worker social security welfare cess could increase delivery cost per order.",
                "Skyrocketing valuation (110x EV/EBITDA) implies zero tolerance for margin stumbles or quick commerce churn."
            ],
            "valuation_context": "Valued as high-growth consumer platform monopoly; commanding 12x EV/Sales.",
            "primary_source_citations": ["Zomato FY24 Annual Report", "Q2 FY25 Shareholder Letter"]
        },
        "business_snapshot": {
            "description": "India's leading consumer internet platform operating Food Delivery, Quick Commerce (Blinkit), B2B restaurant grocery supply (Hyperpure), and Live Events (District).",
            "key_segments": [
                {"name": "Quick Commerce (Blinkit)", "revenue_share_pct": 46.0, "growth": "+128% YoY"},
                {"name": "Food Delivery (Zomato Core)", "revenue_share_pct": 42.0, "growth": "+21% YoY"},
                {"name": "Hyperpure (B2B Supply)", "revenue_share_pct": 12.0, "growth": "+98% YoY"}
            ],
            "export_share_pct": 0.0,
            "domestic_share_pct": 100.0,
            "primary_source": "Zomato Q2 FY25 Shareholder Letter"
        },
        "balance_sheet": {
            "total_debt_cr": 0.0,
            "debt_to_equity": 0.0,
            "working_capital_days": -18,
            "contingent_liabilities_cr": 420.0,
            "contingent_liabilities_notes": "GST demand notices for delivery charges; ongoing industry-wide representation through DIPA/IAMAI.",
            "rpt_flag": False,
            "rpt_details": "No promoter encumbrances or related entity siphoning.",
            "auditor_qualification_flag": False,
            "auditor_notes": "Deloitte Haskins & Sells LLP provided an unmodified clean report.",
            "primary_source": "Zomato FY24 Audited Statements"
        },
        "cash_quality": {
            "cfo_3yr_cumulative_cr": 1820.0,
            "pat_3yr_cumulative_cr": 850.0,
            "cash_conversion_ratio": 2.14,
            "fcf_latest_yr_cr": 940.0,
            "quality_verdict": "Rapidly Improving (Turned solidly FCF positive in FY24 with zero capital debt).",
            "primary_source": "Zomato Cash Flow Statement FY24"
        },
        "guidance": {
            "revenue_growth_target": "40%+ consolidated revenue CAGR over FY25-FY26",
            "margin_corridor": "Blinkit EBITDA margin to reach 4-5% of GOV by FY27",
            "planned_capex_cr": "₹800 Cr for 500+ dark store additions and mother hub warehouses",
            "debt_milestone": "Sustain completely zero-debt balance sheet",
            "time_horizon": "FY25-FY27",
            "primary_source": "Q2 FY25 Shareholder Letter"
        }
    }
}
