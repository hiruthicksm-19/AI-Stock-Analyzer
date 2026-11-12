import asyncio, logging, time
from datetime import datetime, timezone
import requests
from bs4 import BeautifulSoup
from .parsers import parse_number, parse_financial_table
from ..models.financial_data import FinancialDataset, CompanyProfile, PeriodRecord

log = logging.getLogger(__name__)

class ScreenerScraper:
    def __init__(self, session: requests.Session | None = None, delay: float = 1.0, timeout: float = 20):
        self.session = session or requests.Session(); self.delay = delay; self.timeout = timeout

    def fetch(self, name: str, url: str) -> FinancialDataset:
        try:
            time.sleep(max(0, self.delay))
            html = self._crawl_with_crawl4ai(url)
            if html is None:
                r = self.session.get(url, timeout=self.timeout, headers={"User-Agent": "AI-Stock-Research-Agent/1.0"})
                r.raise_for_status(); html = r.text
        except requests.RequestException as exc:
            log.exception("Screener fetch failed")
            raise RuntimeError(f"Screener.in unavailable or restricted: {exc}") from exc
        soup = BeautifulSoup(html, "lxml")
        profile = CompanyProfile(name=name, source_url=url, sector=self._text(soup, "#top .companyInfo h1"), retrieved_at=datetime.now(timezone.utc))
        ratios = {}
        for li in soup.select("#top-ratios li"):
            label = li.select_one(".name"); value = li.select_one(".number")
            if label and value: ratios[label.get_text(" ", strip=True).lower()] = parse_number(value.get_text(" ", strip=True))
        annual = self._records(soup, "profit-loss")
        quarterly = self._records(soup, "quarters")
        balance = self._records(soup, "balance-sheet")
        cash = self._records(soup, "cash-flow")
        warnings = []
        if not annual: warnings.append("Annual profit and loss table was unavailable.")
        return FinancialDataset(company=profile, profit_loss_annual=annual, profit_loss_quarterly=quarterly, balance_sheet_annual=balance, cash_flow_annual=cash, ratios=ratios, warnings=warnings)

    @staticmethod
    def _crawl_with_crawl4ai(url: str) -> str | None:
        """Use Crawl4AI when installed; return None to use the HTTP fallback.

        No authentication, anti-bot bypass, or unrestricted concurrency is used.
        """
        try:
            from crawl4ai import AsyncWebCrawler
        except ImportError:
            return None
        async def run():
            async with AsyncWebCrawler(verbose=False) as crawler:
                result = await crawler.arun(url=url)
                return getattr(result, "html", None) or getattr(result, "raw_html", None)
        try:
            return asyncio.run(run())
        except Exception:
            log.warning("Crawl4AI failed; using compliant requests fallback", exc_info=True)
            return None

    @staticmethod
    def _text(soup, selector):
        node = soup.select_one(selector); return node.get_text(" ", strip=True) if node else None

    def _records(self, soup, table_id):
        table = soup.find("section", id=table_id)
        if not table: return []
        rows = parse_financial_table(str(table))
        periods = []
        for row in rows:
            for period, value in row["values"].items():
                periods.append((period, row["label"], value, row["raw_values"].get(period)))
        grouped = {}
        for period, label, value, raw in periods:
            grouped.setdefault(period, PeriodRecord(period=period)).values[label.lower()] = value
            grouped[period].raw_values[label.lower()] = raw
        return list(grouped.values())

