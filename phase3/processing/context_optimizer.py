import json, re
from datetime import datetime, timezone
from typing import Any
from phase3.models.investment_payload import InvestmentPayload, CompanySummary, Evidence
from phase3.utils.config import Phase3Config

def estimate_tokens(value: Any) -> int:
    text = json.dumps(value, ensure_ascii=False, default=str, separators=(",", ":"))
    return max(1, (len(text) + 3) // 4)

def _short(value: Any, limit: int) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()[:limit]

def _rows(rows: list[dict], limit: int) -> list[dict]:
    out = []
    for row in rows[-limit:]:
        if not isinstance(row, dict): continue
        out.append({"period": row.get("period"), "values": {k: v for k, v in (row.get("values") or {}).items() if v is not None}})
    return out

def build_payload(financial_raw: dict | None, news_raw: dict | None, config: Phase3Config | None = None) -> InvestmentPayload:
    config = config or Phase3Config(); financial_raw = financial_raw or {}; news_raw = news_raw or {}
    d = financial_raw.get("dataset", financial_raw); c = d.get("company", {}) if isinstance(d, dict) else {}
    nc = news_raw.get("company", {}) if isinstance(news_raw, dict) else {}
    company = CompanySummary(name=c.get("name") or nc.get("name") or "Unknown", symbol=nc.get("stock_symbol"), exchange=c.get("exchange") or nc.get("exchange"), sector=c.get("sector") or nc.get("sector"), industry=nc.get("industry"), market_cap=c.get("market_cap"), current_price=c.get("current_price"), currency="INR", source_url=c.get("source_url"))
    metrics = financial_raw.get("metrics", {})
    financial = {"period": "Latest available", "calculated_metrics": metrics, "ratios": {k:v for k,v in (d.get("ratios", {}) or {}).items() if v is not None}, "annual_profit_loss": _rows(d.get("profit_loss_annual", []), config.max_financial_observations), "quarterly_profit_loss": _rows(d.get("profit_loss_quarterly", []), min(8, config.max_financial_observations)), "balance_sheet": _rows(d.get("balance_sheet_annual", []), config.max_financial_observations), "cash_flow": _rows(d.get("cash_flow_annual", []), config.max_financial_observations), "shareholding": _rows(d.get("shareholding", []), config.max_financial_observations), "warnings": d.get("warnings", []) + d.get("retrieval_errors", [])}
    articles = news_raw.get("articles", []) if isinstance(news_raw, dict) else []
    analyses = {a.get("article_url"): a for a in news_raw.get("analyses", [])} if isinstance(news_raw, dict) else {}
    seen, events, news_sources = set(), [], []
    for article in articles:
        url = str(article.get("url", "")); key = (article.get("event_id") or "", re.sub(r"\W", "", article.get("headline", "").lower()))
        if key in seen: continue
        seen.add(key); analysis = analyses.get(url, {}); eid = f"N{len(events)+1:03d}"; categories = article.get("categories") or ["Other"]
        events.append({"event_id": article.get("event_id") or eid, "headline": _short(article.get("headline"), 240), "publisher": article.get("publisher"), "publication_date": article.get("publication_date"), "source_url": url, "category": str(categories[0]), "summary": _short(article.get("summary") or analysis.get("what_happened"), config.max_summary_length), "business_impact": _short(analysis.get("business_impact") or analysis.get("why_it_matters"), 300), "revenue_effect": analysis.get("revenue_effect", "Unknown"), "profitability_effect": analysis.get("profitability_effect", "Unknown"), "capital_or_debt_effect": analysis.get("capital_or_debt_effect", "Unknown"), "risk_or_opportunity": "Risk" if str(article.get("source_type", "")).lower().find("legal") >= 0 else "Opportunity / risk depends on execution", "time_horizon": analysis.get("time_horizon", "Unknown"), "reliability": analysis.get("reliability", "medium"), "verification_status": "Official/confirmed" if "official" in str(article.get("source_type", "")).lower() else "Reported", "evidence_id": eid})
        news_sources.append(Evidence(id=eid, kind="news", label=_short(article.get("headline"), 160), source_url=url, period=article.get("publication_date")))
        if len(events) >= config.max_news_events: break
    fin_sources = [Evidence(id=f"F{i+1:03d}", kind="financial", label=f"Financial statements {row.get('period')}", source_url=company.source_url, period=row.get("period")) for i, row in enumerate(financial["annual_profit_loss"])]
    payload = InvestmentPayload(company=company, financial_analysis=financial, business_intelligence={"research_period": news_raw.get("report", {}).get("research_period") if isinstance(news_raw.get("report"), dict) else None, "events": events, "warnings": news_raw.get("warnings", [])}, evidence={"financial_sources": fin_sources, "news_sources": news_sources}, metadata={"financial_retrieved_at": c.get("retrieved_at"), "news_retrieved_at": nc.get("retrieved_at"), "payload_created_at": datetime.now(timezone.utc).isoformat(), "selected_news_events": len(events), "excluded_news_events": max(0, len(articles)-len(events))})
    payload.metadata["estimated_input_tokens"] = estimate_tokens(payload.model_dump(mode="json"))
    if payload.metadata["estimated_input_tokens"] > max(1, config.max_input_tokens - config.system_prompt_reserve - config.output_token_reserve):
        payload.metadata["budget_warning"] = "Payload exceeds configured analysis budget after deterministic selection."
    return payload

