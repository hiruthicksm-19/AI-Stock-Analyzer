from phase3.models.workflow import WorkflowResult, StageResult
from phase3.adapters.phase1_adapter import Phase1Adapter
from phase3.adapters.phase2_adapter import Phase2Adapter
from phase3.processing.context_optimizer import build_payload
from phase3.processing.data_validator import validate_financial, validate_news
from phase3.llm.investment_analyst import InvestmentAnalyst

class ResearchOrchestrator:
    def __init__(self, phase1=None, phase2=None, analyst=None, config=None):
        self.phase1 = phase1 or Phase1Adapter(); self.phase2 = phase2 or Phase2Adapter(); self.analyst = analyst or InvestmentAnalyst(); self.config = config
    def run(self, query: str, selected_url: str | None = None, selected_company=None, research_days: int = 90) -> WorkflowResult:
        out = WorkflowResult(query=query); out.stages.append(StageResult("company_identification", "complete", "Company input accepted."))
        try:
            financial = self.phase1.run(query, selected_url=selected_url); 
            if "matches" in financial: raise ValueError("Multiple Phase 1 company matches require confirmation.")
            out.financial_raw = self.phase1.raw_dict(financial); vf = validate_financial(out.financial_raw)
            if not vf.valid: raise ValueError("; ".join(vf.errors))
            out.stages += [StageResult("financial_collection", "complete"), StageResult("financial_validation", "complete", "; ".join(vf.warnings))]
        except Exception as exc:
            out.errors.append(f"Phase 1: {exc}"); out.partial = True; out.stages.append(StageResult("financial_collection", "failed", str(exc)))
        company = selected_company or (out.financial_raw.get("dataset", {}).get("company", {}).get("name") if out.financial_raw else query)
        try:
            news = self.phase2.run(company, days=research_days); out.news_raw = self.phase2.raw_dict(news); vn = validate_news(out.news_raw)
            if not vn.valid: raise ValueError("; ".join(vn.errors))
            out.stages += [StageResult("news_collection", "complete"), StageResult("news_validation", "complete", "; ".join(vn.warnings))]
        except Exception as exc:
            out.errors.append(f"Phase 2: {exc}"); out.partial = True; out.stages.append(StageResult("news_collection", "failed", str(exc)))
        payload = build_payload(out.financial_raw, out.news_raw, self.config); out.optimized_payload = payload.model_dump(mode="json"); out.stages.append(StageResult("json_optimization", "complete"))
        if not out.financial_raw or not out.news_raw:
            out.partial = True; out.errors.append("Combined assessment is partial because one agent did not return data.")
        try:
            out.report, usage = self.analyst.analyze(payload); out.stages.append(StageResult("llm_analysis", "complete", usage.analysis_status, usage.as_dict()))
        except Exception as exc:
            out.errors.append(f"LLM: {exc}"); out.stages.append(StageResult("llm_analysis", "failed", str(exc)))
        return out

