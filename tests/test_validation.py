import pytest
from stock_research_agent.models.financial_data import FinancialDataset, CompanyProfile, PeriodRecord
from stock_research_agent.models.research_report import ResearchReport

def test_json_validation_round_trip():
    d = FinancialDataset(company=CompanyProfile(name="X", source_url="https://x"), warnings=["missing"])
    assert FinancialDataset.model_validate_json(d.model_dump_json()).company.name == "X"

def test_report_validation_rejects_unknown_assessment():
    with pytest.raises(ValueError):
        ResearchReport(company_name="X", assessment="buy", company_overview="", financial_performance="", growth_analysis="", profitability_analysis="", financial_health="", shareholding_analysis="", valuation_analysis="", conclusion="")

def test_report_accepts_structured_llm_sections():
    report = ResearchReport(company_name="X", assessment="Mixed fundamentals", company_overview="", financial_performance={"revenue_trend": []}, growth_analysis={"cagr": 0.1}, profitability_analysis={"roe": 0.2}, financial_health={"debt": 0}, shareholding_analysis={"promoter": 50}, valuation_analysis={"pe": 15}, conclusion="ok")
    assert '"revenue_trend"' in report.financial_performance
    assert '"cagr"' in report.growth_analysis

def test_parse_json_object_handles_fenced_json():
    from stock_research_agent.llm.analyst import Analyst
    assert Analyst._parse_json_object("```json\n{\"ok\": true}\n```") == {"ok": True}

