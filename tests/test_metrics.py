from stock_research_agent.analysis.financial_metrics import cagr, growth, calculate_metrics
from stock_research_agent.models.financial_data import FinancialDataset, CompanyProfile, PeriodRecord

def test_growth_and_cagr():
    assert growth([100, 120, 0]) == [None, .2, None]
    assert round(cagr(100, 121, 2), 6) == .1
    assert cagr(-100, 121, 2) is None

def test_metrics_uses_financial_data():
    d = FinancialDataset(company=CompanyProfile(name="Test", source_url="https://example"), profit_loss_annual=[PeriodRecord(period=str(y), values={"sales": s, "net profit": p}) for y,s,p in [(2022,100,10),(2023,120,12),(2024,144,18)]], ratios={"roe": .15})
    m = calculate_metrics(d)
    assert m["revenue_growth_yoy"][-1] == .2
    assert m["ratios"]["roe"] == .15

