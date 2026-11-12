from datetime import date
from phase2.agent.intelligence_agent import run_company_intelligence
from phase2.models.company import CompanyProfile

class EmptySearch:
    def search(self, *args, **kwargs): return []

def test_confirmed_profile_is_not_reidentified():
    selected=CompanyProfile(name="Hexaware Technologies Limited", stock_symbol="HEXT", exchange="NSE", verified=False)
    result=run_company_intelligence(selected, start_date=date.today(), end_date=date.today(), search_engine=EmptySearch(), persist=False)
    assert result.company.stock_symbol == "HEXT"
