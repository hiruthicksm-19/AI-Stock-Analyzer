from ..scraper.company_search import search_company
from ..scraper.screener_scraper import ScreenerScraper
from ..analysis.financial_metrics import calculate_metrics
from ..llm.analyst import Analyst

class StockResearchAgent:
    def __init__(self, searcher=search_company, scraper=None, analyst=None):
        self.searcher, self.scraper, self.analyst = searcher, scraper or ScreenerScraper(), analyst or Analyst()

    def run(self, query: str, selected_url: str | None = None):
        matches = self.searcher(query)
        if not matches: raise ValueError(f"No Screener.in company matched '{query}'.")
        if selected_url is None and len(matches) > 1: return {"matches": matches}
        match = next((m for m in matches if m.url == selected_url), matches[0])
        data = self.scraper.fetch(match.name, match.url)
        metrics = calculate_metrics(data)
        report = self.analyst.generate(data, metrics)
        return {"dataset": data, "metrics": metrics, "report": report}

