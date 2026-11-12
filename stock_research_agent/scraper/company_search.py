from dataclasses import dataclass
from urllib.parse import quote_plus
import re
import requests
from bs4 import BeautifulSoup

@dataclass(frozen=True)
class CompanyMatch:
    name: str
    url: str
    symbol: str | None = None

def search_company(query: str, session: requests.Session | None = None, timeout: float = 15) -> list[CompanyMatch]:
    query = " ".join(query.split())
    if not query: return []
    sess = session or requests.Session()
    url = f"https://www.screener.in/api/company/search/?q={quote_plus(query)}"
    try:
        response = sess.get(url, timeout=timeout, headers={"User-Agent": "AI-Stock-Research-Agent/1.0"})
        response.raise_for_status()
        data = response.json()
        rows = data if isinstance(data, list) else data.get("results", [])
        matches = []
        for row in rows:
            name = str(row.get("name", "")).strip()
            link = str(row.get("url", row.get("link", ""))).strip()
            if name and link:
                if link.startswith("/"): link = "https://www.screener.in" + link
                matches.append(CompanyMatch(name, link, row.get("id") and str(row["id"])))
        return matches
    except (requests.RequestException, ValueError):
        return []

