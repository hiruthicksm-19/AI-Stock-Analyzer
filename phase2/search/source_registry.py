from dataclasses import dataclass

@dataclass(frozen=True)
class SourceConfig:
    name: str
    url: str
    source_type: str
    enabled: bool = True
    rss_url: str | None = None
    notes: str = ""

def default_sources() -> list[SourceConfig]:
    rows = [("NSE India", "https://www.nseindia.com/", "official_exchange_disclosure"), ("BSE India", "https://www.bseindia.com/", "official_exchange_disclosure"), ("Moneycontrol", "https://www.moneycontrol.com/", "financial_news"), ("Economic Times Markets", "https://economictimes.indiatimes.com/markets", "financial_news"), ("Business Standard", "https://www.business-standard.com/", "financial_news"), ("Mint", "https://www.livemint.com/", "financial_news"), ("CNBC-TV18", "https://www.cnbctv18.com/", "financial_news"), ("Reuters Markets", "https://www.reuters.com/markets/", "financial_news"), ("Business Wire", "https://www.businesswire.com/", "company_press_release"), ("PR Newswire", "https://www.prnewswire.com/", "company_press_release"), ("GlobeNewswire", "https://www.globenewswire.com/", "company_press_release"), ("CRISIL", "https://www.crisil.com/", "credit_rating_report"), ("ICRA", "https://www.icra.in/", "credit_rating_report"), ("India Ratings", "https://www.indiaratings.co.in/", "credit_rating_report"), ("CARE Edge", "https://www.careedge.in/", "credit_rating_report"), ("RBI", "https://www.rbi.org.in/", "government_source"), ("SEBI", "https://www.sebi.gov.in/", "government_source"), ("PIB", "https://www.pib.gov.in/", "government_source"), ("IBEF", "https://www.ibef.org/", "industry_report"), ("NITI Aayog", "https://www.niti.gov.in/", "government_source")]
    return [SourceConfig(*r) for r in rows]
