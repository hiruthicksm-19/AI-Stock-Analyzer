import pytest
from phase2.company.company_search import CompanySearch, AmbiguousCompanyError
def test_alias_and_symbol_identification():
    assert CompanySearch().identify("INFY").name == "Infosys Limited"
    assert CompanySearch().identify("Infosys Ltd").stock_symbol == "INFY"
def test_missing_company_is_explicit():
    profile=CompanySearch().identify("TECHM")
    assert profile.stock_symbol == "TECHM"
    generic=CompanySearch().identify("Acme Industries")
    assert generic.verified is False and generic.stock_symbol is None

def test_remote_lookup_maps_indian_listing(monkeypatch):
    class Response:
        def raise_for_status(self): pass
        def json(self): return {"quotes":[{"symbol":"ABC.NS","longname":"ABC Industries Limited","sector":"Industrials","industry":"Engineering"}]}
    monkeypatch.setattr("phase2.company.company_search.requests.get", lambda *args, **kwargs: Response())
    profile=CompanySearch(allow_remote=True).identify("ABC Industries")
    assert profile.stock_symbol == "ABC" and profile.exchange == "NSE" and profile.verified is False

def test_identify_accepts_selected_profile_object():
    profile=CompanySearch().identify(type("Selected", (), {"name":"Hexaware", "model_dump":lambda self:{}})())
    assert profile.name == "Hexaware"
