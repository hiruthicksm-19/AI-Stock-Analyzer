from datetime import datetime, timezone
from pathlib import Path
from phase2.models.article import Article, SourceType
from phase2.scraper.article_extractor import ArticleExtractor
from phase2.database.db import Database
from phase2.database.repository import Repository
from phase2.models.company import CompanyProfile
from phase2.models.report import CompanyIntelligenceReport, ResearchResult
def test_extractor_removes_navigation():
    class Response:
        text='<html><nav>Menu</nav><article><h1>Real title</h1><p>Company factory expansion.</p></article></html>'
        def raise_for_status(self): pass
    class Session:
        def get(self, *args, **kwargs): return Response()
    a=ArticleExtractor(session=Session()).extract('https://example.com/a','Company')
    assert a.accessible_content and 'Menu' not in a.content and 'factory expansion' in a.content

def test_extractor_follows_redirect_and_uses_article_body():
    class Response:
        url='https://publisher.example/news/1'
        text='<article><h1>ICICI announces a new trade agreement</h1><p>The bank signed an agreement to support cross-border trade.</p></article>'
        def raise_for_status(self): pass
    class Session:
        def get(self, *args, **kwargs): return Response()
    a=ArticleExtractor(session=Session()).extract('https://news.google.com/rss/articles/example','ICICI Bank', 'ICICI agreement', 'Publisher', rss_summary='<p>RSS description</p>')
    assert str(a.url) == 'https://publisher.example/news/1' and 'cross-border trade' in a.content
def test_database_schema_is_independent(tmp_path: Path):
    db=Database(tmp_path/'phase2.sqlite3')
    with db.connect() as c: names={r[0] for r in c.execute("select name from sqlite_master where type='table'")}
    assert {'companies','articles','reports'} <= names

def test_research_is_saved_as_json(tmp_path: Path):
    result=ResearchResult(company=CompanyProfile(name="Test Company"), report=CompanyIntelligenceReport(company_information={"name":"Test Company"}))
    path=Repository(Database(tmp_path/'db.sqlite3')).save_json(result, tmp_path/'reports')
    assert path.exists() and path.suffix == ".json"
