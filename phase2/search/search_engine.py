from datetime import datetime
from urllib.parse import quote_plus
try:
    import feedparser
except ImportError:
    feedparser = None
from ..scraper.rss_reader import parse_feed
from ..models.article import Article, SourceType

class SearchEngine:
    def __init__(self, sources=None, timeout=15): self.sources = sources or []; self.timeout = timeout
    def search_rss(self, query: str, company_name: str, start_date=None, end_date=None) -> list[Article]:
        feed = feedparser.parse(f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-IN&gl=IN&ceid=IN:en") if feedparser else None
        articles=[]; now=datetime.now().astimezone()
        entries = [{"title": x.get("title", "Untitled"), "link": x.get("link", ""), "summary": x.get("summary", ""), "publisher": x.get("source", {}).get("title", "Google News RSS"), "published": datetime(*x.published_parsed[:6]) if getattr(x, "published_parsed", None) else None} for x in (feed.entries[:30] if feedparser else [])]
        for entry in entries:
            published = entry["published"].astimezone() if entry["published"] else None
            if start_date and published and published.date() < start_date: continue
            if end_date and published and published.date() > end_date: continue
            articles.append(Article(headline=entry.get("title", "Untitled"), url=entry.get("link"), publisher=entry["publisher"], publication_date=published, retrieved_at=now, summary=entry.get("summary", ""), company_name=company_name, source_type=SourceType.FINANCIAL_NEWS, accessible_content=False))
        return articles
    def search(self, queries, company_name, start_date=None, end_date=None):
        output=[]
        for query in queries[:12]: output.extend(self.search_rss(query, company_name, start_date, end_date))
        tokens=[token.lower() for token in company_name.replace("limited", "").replace("ltd", "").split() if len(token)>3]
        noise=("stock price", "stock forecast", "analyst predictions", "brokerage charges", "stocks to buy", "price history", "share price")
        return [article for article in output if (not tokens or any(token in (article.headline+" "+article.summary).lower() for token in tokens)) and not any(term in (article.headline+" "+article.summary).lower() for term in noise)]
