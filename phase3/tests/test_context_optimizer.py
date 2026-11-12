from phase3.processing.context_optimizer import build_payload, estimate_tokens

def test_optimizer_bounds_news_and_preserves_sources():
    financial = {"dataset": {"company": {"name":"Acme", "source_url":"https://screener.in/acme"}, "profit_loss_annual": [{"period":"2024", "values":{"sales":100}}], "ratios":{"pe":10}}, "metrics": {"revenue_cagr_3y": 0.1}}
    news = {"company": {"name":"Acme"}, "articles": [{"headline":f"Event {i}","url":f"https://x/{i}","publisher":"P","summary":"fact"} for i in range(4)], "analyses": []}
    payload = build_payload(financial, news)
    assert payload.company.source_url.endswith("acme")
    assert len(payload.business_intelligence["events"]) == 4
    assert estimate_tokens(payload.model_dump()) > 0

