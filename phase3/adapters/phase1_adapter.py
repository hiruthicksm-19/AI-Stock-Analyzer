from typing import Any

class Phase1Adapter:
    """Calls Phase 1's public agent interface and preserves its raw output."""
    def __init__(self, agent=None):
        if agent is None:
            from stock_research_agent.agent.stock_agent import StockResearchAgent
            agent = StockResearchAgent()
        self.agent = agent

    def identify(self, query: str) -> list[Any]:
        from stock_research_agent.scraper.company_search import search_company
        return search_company(query)

    def run(self, query: str, selected_url: str | None = None) -> dict:
        result = self.agent.run(query, selected_url=selected_url)
        if "matches" in result:
            return {"matches": result["matches"]}
        if not result.get("dataset"):
            raise ValueError("Phase 1 returned no financial dataset.")
        return result

    @staticmethod
    def raw_dict(result: dict) -> dict:
        dataset = result.get("dataset")
        return {
            "dataset": dataset.as_dict() if hasattr(dataset, "as_dict") else dataset,
            "metrics": result.get("metrics", {}),
            "report": result.get("report").model_dump(mode="json") if hasattr(result.get("report"), "model_dump") else result.get("report"),
        }

