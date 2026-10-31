# Covering note (draft: edit before sending)

**To:** assessment@enam.com
**Subject:** ENAM - IIT screening - 2027

**Prototype:** [ADD DEPLOYED LINK]
**Repository:** [ADD GITHUB LINK]
**AI build history:** [ADD LINKS OR ATTACHMENTS]

## What I built
FINN is a mobile-first web app for an investor following 18 NSE stocks.

- **Push:** a digest with selectable time windows, where routine filings are collapsed, plus price and volume alerts with adjustable thresholds and a spoken briefing.
- **Pull:** a search for any NSE ticker that returns live figures and links to annual reports and concalls, plus deeper research views for five sample companies, led by a promises-vs-delivery table.

## Key decisions and trade-offs
- **Focus on filtering:** priority ordering, collapsed routine filings and user-set thresholds keep the first screen short.
- **Honest gaps over invented answers:** an unknown ticker returns "No data found", and a company without analysis shows "Not assessed". Sample data is labelled in the app.
- **Mobile interaction:** bottom navigation, sliders for alert thresholds and an audio briefing for a commute, using the browser's own speech engine at no cost.
- **Simple hosting:** FastAPI serves the built frontend, so the app deploys as one free service.

## What I deliberately left out
- **Live filings:** the digest uses 20 hand-written sample filings, not the NSE/BSE feed.
- **LLM analysis:** the deeper research views are hand-written and have not been checked against the filings. They show the intended product, not a working analysis engine.
- **Other research views:** there is no multi-year trajectory view yet.

## Where I'd take it next
1. Connect the live NSE/BSE feed and improve the classifier on real filings.
2. Generate promises vs delivery from real transcripts and results, with a citation for each claim, using a cheap model for extraction and a stronger one for reasoning.
3. Add push notifications for triggered alerts.
