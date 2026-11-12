from datetime import datetime
try:
    import feedparser
except ImportError:
    feedparser = None
from xml.etree import ElementTree

def parse_feed(xml: str) -> list[dict]:
    if feedparser:
        feed = feedparser.parse(xml); entries = feed.entries
        return [{"headline": e.get("title", ""), "url": e.get("link", ""), "summary": e.get("summary", ""), "publication_date": datetime(*e.published_parsed[:6]) if getattr(e, "published_parsed", None) else None} for e in entries]
    root=ElementTree.fromstring(xml); rows=[]
    for item in root.findall(".//item"):
        rows.append({"headline": item.findtext("title", ""), "url": item.findtext("link", ""), "summary": item.findtext("description", ""), "publication_date": None})
    return rows
