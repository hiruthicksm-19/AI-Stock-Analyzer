import re
import requests
from urllib.parse import quote_plus
from .company_profile import KNOWN_COMPANIES
from ..models.company import CompanyProfile

class AmbiguousCompanyError(ValueError): pass

def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.lower().replace("limited", "").replace("ltd", ""))

class CompanySearch:
    def __init__(self, profiles=None, allow_remote=False, timeout=6):
        self.profiles = profiles or KNOWN_COMPANIES
        self.allow_remote = allow_remote
        self.timeout = timeout
    def _remote_find(self, query: str) -> list[CompanyProfile]:
        """Best-effort public lookup; metadata remains unverified until confirmed."""
        try:
            response=requests.get(f"https://query1.finance.yahoo.com/v1/finance/search?q={quote_plus(query)}&quotesCount=20&newsCount=0", timeout=self.timeout, headers={"User-Agent":"Phase2-Company-Intelligence/1.0"})
            response.raise_for_status()
            results=[]
            for quote in response.json().get("quotes", []):
                symbol=quote.get("symbol", "")
                if not (symbol.endswith(".NS") or symbol.endswith(".BO")): continue
                ticker=symbol.rsplit(".", 1)[0]
                results.append(CompanyProfile(name=quote.get("longname") or quote.get("shortname") or ticker, stock_symbol=ticker, exchange="NSE" if symbol.endswith(".NS") else "BSE", sector=quote.get("sector"), industry=quote.get("industry"), confidence=0.6, verified=False))
            return results
        except Exception:
            return []
    def find(self, query: str) -> list[CompanyProfile]:
        q = _norm(query.strip())
        if not q: return []
        matches = [p for p in self.profiles if q == _norm(p.name) or q == _norm(p.stock_symbol or "") or any(q == _norm(a) for a in p.aliases)]
        if matches: return matches
        matches=[p for p in self.profiles if q in _norm(p.name) or any(q in _norm(a) for a in p.aliases)]
        if matches or not self.allow_remote: return matches
        return self._remote_find(query)
    def identify(self, query: str, selected: CompanyProfile | None = None) -> CompanyProfile:
        if isinstance(query, CompanyProfile): return query
        if hasattr(query, "name") and hasattr(query, "model_dump"):
            return query
        matches = self.find(query)
        if selected: return selected
        if not matches:
            cleaned=query.strip()
            if not cleaned: raise LookupError("Enter a company name or stock symbol.")
            is_symbol=bool(re.fullmatch(r"[A-Za-z0-9.-]{2,20}", cleaned)) and " " not in cleaned
            return CompanyProfile(name=cleaned, stock_symbol=cleaned.upper() if is_symbol else None, exchange="NSE/BSE" if is_symbol else None, aliases=[cleaned], confidence=0.25, verified=False)
        if len(matches) > 1: raise AmbiguousCompanyError(f"Multiple companies matched '{query}'. Please confirm the exact company.")
        return matches[0]
