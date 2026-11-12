import json
import re
from datetime import datetime, timezone
from pathlib import Path
class Repository:
    def __init__(self, db): self.db=db
    def save_json(self, result, directory=None):
        target=Path(directory or Path(__file__).parents[1]/"storage"/"reports")
        target.mkdir(parents=True, exist_ok=True)
        slug=re.sub(r"[^a-z0-9]+", "_", result.company.name.lower()).strip("_") or "company"
        stamp=datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        path=target/f"{slug}_{stamp}.json"
        path.write_text(json.dumps(result.model_dump(mode="json"), indent=2, ensure_ascii=False), encoding="utf-8")
        return path
    def save_research(self, result):
        with self.db.connect() as c:
            cur=c.execute("INSERT INTO companies(name,stock_symbol,exchange,profile_json) VALUES(?,?,?,?)", (result.company.name,result.company.stock_symbol,result.company.exchange,result.company.model_dump_json())); company_id=cur.lastrowid
            for article, analysis in zip(result.articles, result.analyses): c.execute("INSERT OR IGNORE INTO articles(company_id,url,headline,publisher,publication_date,retrieved_at,content,summary,source_type,categories,event_id,analysis_json) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)",(company_id,str(article.url),article.headline,article.publisher,str(article.publication_date or ""),str(article.retrieved_at),article.content,article.summary,article.source_type.value,json.dumps([x.value for x in article.categories]),article.event_id,analysis.model_dump_json()))
            c.execute("INSERT INTO reports(company_id,created_at,report_json) VALUES(?,?,?)",(company_id,datetime.now(timezone.utc).isoformat(),result.report.model_dump_json()))
