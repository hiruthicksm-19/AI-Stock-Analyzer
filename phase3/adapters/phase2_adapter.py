from datetime import date, timedelta
from typing import Any

class Phase2Adapter:
    """Calls Phase 2's public intelligence workflow without changing its internals."""
    def __init__(self, runner=None, searcher=None):
        if runner is None:
            from phase2.agent.intelligence_agent import run_company_intelligence
            runner = run_company_intelligence
        self.runner = runner
        self.searcher = searcher

    def identify(self, query: str) -> list[Any]:
        from phase2.company.company_search import CompanySearch
        return (self.searcher or CompanySearch(allow_remote=True)).find(query)

    def run(self, company: Any, days: int = 90) -> Any:
        return self.runner(company, start_date=date.today() - timedelta(days=days), end_date=date.today(), persist=False)

    @staticmethod
    def raw_dict(result: Any) -> dict:
        return result.model_dump(mode="json") if hasattr(result, "model_dump") else dict(result)

