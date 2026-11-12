# AI Stock Research Analyst

Phase 1 fundamental research for Indian listed companies using publicly accessible Screener.in data. The app does not provide a buy/sell recommendation or price prediction.

## Run

```powershell
python -m pip --timeout 300 --retries 10 install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

`GROQ_API_KEY` is required for AI prose. Without it, the app still displays the verified data and deterministic metrics and explains how to configure the Groq provider.

## Design

`scraper/` owns company discovery, Crawl4AI-first/requests-fallback access, and HTML parsing. Playwright is available to Crawl4AI for pages requiring browser rendering, but the app does not bypass authentication or anti-bot controls. `models/` defines validated data contracts. `analysis/` computes metrics independently of the LLM. `llm/` only interprets the validated payload. `agent/` orchestrates the controlled workflow, and `app.py` is the frontend adapter.

Automated tests use mocked HTML and synthetic financial data; they never call Screener.in.

