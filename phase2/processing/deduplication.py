import hashlib, re
from urllib.parse import urlsplit, urlunsplit
from difflib import SequenceMatcher

def canonicalize_url(url: str) -> str:
    p=urlsplit(str(url)); return urlunsplit((p.scheme.lower(), p.netloc.lower(), p.path.rstrip("/"), "", ""))
def _headline(value): return re.sub(r"[^a-z0-9]", "", value.lower())
def group_duplicates(articles):
    groups=[]; kept=[]
    for article in articles:
        found=None
        for group in groups:
            other=group["articles"][0]; similarity=SequenceMatcher(None, _headline(article.headline), _headline(other.headline)).ratio()
            if canonicalize_url(article.url)==canonicalize_url(other.url) or similarity >= .86: found=group; break
        if not found:
            event_id=hashlib.sha1(_headline(article.headline).encode()).hexdigest()[:16]; found={"event_id":event_id,"articles":[]}; groups.append(found); kept.append(article)
        found["articles"].append(article); article.event_id=found["event_id"]
    return groups, kept
