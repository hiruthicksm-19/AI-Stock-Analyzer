import json
from phase3.models.investment_payload import InvestmentPayload, InvestmentReport
from phase3.llm.client import Phase3LLMClient
from phase3.llm.prompts import SYSTEM_PROMPT
from phase3.llm.token_tracker import TokenUsage
from phase3.processing.context_optimizer import estimate_tokens

class InvestmentAnalyst:
    def __init__(self, client=None): self.client = client or Phase3LLMClient()
    def analyze(self, payload: InvestmentPayload):
        raw = payload.model_dump(mode="json"); usage = TokenUsage(self.client.model, estimate_tokens(raw), selected_news_events=payload.metadata.get("selected_news_events", 0), excluded_news_events=payload.metadata.get("excluded_news_events", 0), payload_size_bytes=len(json.dumps(raw, default=str).encode()))
        if payload.metadata.get("budget_warning"): usage.analysis_status = "rejected_budget"; return InvestmentReport(conclusion="The optimized payload exceeds the configured token budget; no assessment was generated."), usage
        try:
            result, provider_usage = self.client.complete_json(SYSTEM_PROMPT, raw)
            if result is None:
                usage.analysis_status = "fallback_no_api_key"; return self._fallback(payload), usage
            report = InvestmentReport.model_validate(result); usage.analysis_status = "complete"
            if provider_usage:
                usage.actual_input_tokens = getattr(provider_usage, "prompt_tokens", None); usage.output_tokens = getattr(provider_usage, "completion_tokens", None); usage.total_tokens = getattr(provider_usage, "total_tokens", None)
            return report, usage
        except Exception as exc:
            usage.analysis_status = f"failed: {type(exc).__name__}"; raise RuntimeError(f"Phase 3 LLM analysis failed: {exc}") from exc
    @staticmethod
    def _fallback(payload):
        has_fin = bool(payload.financial_analysis.get("annual_profit_loss")); has_news = bool(payload.business_intelligence.get("events")); stance = "WATCH / WAIT" if has_fin and has_news else "INSUFFICIENT DATA"
        return InvestmentReport(stance=stance, confidence="low", company_overview=f"{payload.company.name} was processed from the available Phase 1 and Phase 2 evidence.", executive_summary="No Phase 3 LLM API key is configured; this is a deterministic status summary, not an investment recommendation.", negative_factors=["Combined LLM narrative is unavailable."], conclusion="Configure GROQ_API_KEY to generate the evidence-based combined assessment.", evidence_ids=[x.id for xs in payload.evidence.values() for x in xs])

