from datetime import datetime
import requests
from bs4 import BeautifulSoup
from html import unescape
import re
from ..models.article import Article, SourceType

class ArticleExtractor:
    def __init__(self, timeout=20, session=None): self.timeout=timeout; self.session=session or requests.Session()
    def extract(self, url: str, company_name: str, headline: str = "", publisher: str = "Unknown", source_type=SourceType.OTHER, publication_date=None, rss_summary: str = "") -> Article:
        now=datetime.now().astimezone()
        try:
            response=self.session.get(url, timeout=self.timeout, allow_redirects=True, headers={"User-Agent":"Phase2-Company-Intelligence/1.0 (respectful research client)"}); response.raise_for_status()
            soup=BeautifulSoup(response.text, "lxml")
            for node in soup.select("script,style,nav,header,footer,aside,form,.advertisement,.ads"): node.decompose()
            title=headline or (soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else soup.title.get_text(" ", strip=True) if soup.title else "Untitled")
            body=soup.find("article") or soup.find("main") or soup.body; content=" ".join(body.stripped_strings) if body else ""
            fallback=re.sub(r"\s+", " ", unescape(BeautifulSoup(rss_summary or "", "html.parser").get_text(" ", strip=True))).strip()
            return Article(headline=title, url=getattr(response, "url", None) or url, publisher=publisher, publication_date=publication_date, retrieved_at=now, content=content[:50000], summary=(content[:600] if content else fallback), company_name=company_name, source_type=source_type, accessible_content=bool(content))
        except Exception as exc:
            fallback=re.sub(r"\s+", " ", unescape(BeautifulSoup(rss_summary or "", "html.parser").get_text(" ", strip=True))).strip()
            return Article(headline=headline or "Inaccessible article", url=url, publisher=publisher, publication_date=publication_date, retrieved_at=now, summary=fallback, company_name=company_name, source_type=source_type, accessible_content=False, retrieval_error=str(exc))
