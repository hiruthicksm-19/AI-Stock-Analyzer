from stock_research_agent.agent.stock_agent import StockResearchAgent
from stock_research_agent.llm.analyst import Analyst
from stock_research_agent.scraper.company_search import CompanyMatch
from stock_research_agent.models.financial_data import FinancialDataset, CompanyProfile
from stock_research_agent.models.research_report import ResearchReport

class FakeScraper:
    def fetch(self, name, url): return FinancialDataset(company=CompanyProfile(name=name, source_url=url))

class FakeAnalyst:
    def generate(self, data, metrics): return ResearchReport(company_name=data.company.name, assessment="Insufficient data", company_overview="", financial_performance="", growth_analysis="", profitability_analysis="", financial_health="", shareholding_analysis="", valuation_analysis="", conclusion="")

def test_agent_requires_selection_for_multiple_matches():
    matches = lambda q: [CompanyMatch("A", "https://a"), CompanyMatch("B", "https://b")]
    out = StockResearchAgent(matches, FakeScraper(), FakeAnalyst()).run("a")
    assert len(out["matches"]) == 2

def test_agent_passes_data_through_analysis_and_report():
    matches = lambda q: [CompanyMatch("A", "https://a")]
    out = StockResearchAgent(matches, FakeScraper(), FakeAnalyst()).run("a")
    assert out["dataset"].company.source_url == "https://a"
    assert out["report"].assessment == "Insufficient data"

def test_llm_payload_removes_duplicate_raw_values():
    from stock_research_agent.models.financial_data import PeriodRecord
    data = FakeScraper().fetch("A", "https://a")
    data.profit_loss_annual = [PeriodRecord(period="2024", values={"sales": 100}, raw_values={"sales": "₹100 crore"})]
    compact = Analyst._compact_payload(data, {"revenue_cagr_3y": None})
    assert compact["profit_loss_annual"] == [{"period": "2024", "values": {"sales": 100}}]

