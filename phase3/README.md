# Phase 3 — Unified Investment Research & Decision Agent

Phase 3 is an independent integration layer. It imports Phase 1's `StockResearchAgent` and Phase 2's `run_company_intelligence` through adapters; it does not modify either implementation or replace either Streamlit app. Phase 3 uses only the Groq-compatible `openai/gpt-oss-120b` model; alternate model configuration is ignored.

## Run

From the project root:

```powershell
Copy-Item phase3/.env.example phase3/.env
streamlit run phase3/app.py
```

Without `GROQ_API_KEY`, the app still validates, optimizes, and displays provenance, but the report is explicitly marked as a deterministic fallback. No financial or news values are invented.

## Optimization

The optimizer keeps calculated financial metrics, bounded recent observations, warnings, and at most `MAX_NEWS_EVENTS` unique news events. It removes article bodies, duplicate headlines, null metrics, and irrelevant metadata. It estimates tokens conservatively at approximately four characters per token, reserves prompt/output budget, records excluded events, and rejects the LLM call if the configured budget is exceeded.

## Evidence

Financial evidence is assigned `F001...`; news evidence is assigned `N001...`. Source URLs and reporting periods are retained in the optimized payload so report claims can be traced back to the original datasets.

