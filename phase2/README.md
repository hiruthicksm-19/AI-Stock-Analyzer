# AI Company Intelligence Agent — Phase 2

Phase 2 is an independent company-news and business-intelligence agent. It lives entirely under `phase2/`, uses its own SQLite database, and does not import or modify the existing Phase 1 application.

## Install and run

Use the existing Phase 1 environment from the project root:

```powershell
venv\Scripts\Activate.ps1
venv\Scripts\python.exe -m pip install -r phase2\requirements.txt
Copy-Item phase2\.env.example phase2\.env
venv\Scripts\python.exe -m streamlit run phase2\app.py
```

`GROQ_API_KEY` is optional. Without it, deterministic evidence-aware analysis is used and the UI clearly reports the limitation. `SEARCH_API_KEY` is reserved for a future provider adapter; the current default uses public Google News RSS results and does not claim exhaustive real-time coverage.

## Architecture

Company identification uses the built-in verified examples first, then a best-effort public Yahoo Finance lookup for NSE/BSE symbols, and finally an explicitly unverified fallback so arbitrary company names can still be researched. The rest of the flow is query generation → RSS search-provider abstraction → compliant HTTP/BeautifulSoup extraction → cleaning → URL/headline deduplication → multi-label classification → heuristic or Groq article analysis → SQLite persistence → Streamlit report/dashboard.

The public-source registry includes NSE, BSE, Moneycontrol, Economic Times Markets, Business Standard, Mint, CNBC-TV18, Reuters, Business Wire, PR Newswire, GlobeNewswire, CRISIL, ICRA, India Ratings, CARE Edge, RBI, SEBI, PIB, IBEF and NITI Aayog. Sites remain configurable and inaccessible/blocked sources are recorded as warnings; paywalls, authentication and anti-bot controls are not bypassed.

## Tests

From the project root, run `python -m pytest phase2/tests -q`. Tests use mocked HTML/RSS and do not depend on live websites.

The callable integration boundary is `phase2.run_company_intelligence(company_name, stock_symbol=None, start_date=None, end_date=None)`. Each persisted run is also written as a timestamped JSON file under `phase2/storage/reports/`, in addition to SQLite storage.
