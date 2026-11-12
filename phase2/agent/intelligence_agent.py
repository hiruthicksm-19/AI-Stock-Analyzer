from datetime import date, timedelta
from ..company.company_search import CompanySearch
from ..search.query_generator import generate_queries
from ..search.search_engine import SearchEngine
from ..scraper.article_extractor import ArticleExtractor
from ..processing.article_cleaner import clean_article
from ..processing.deduplication import group_duplicates
from ..processing.article_classifier import classify_article
from ..analysis.article_analyzer import ArticleAnalyzer
from ..analysis.company_intelligence import build_report
from ..models.report import ResearchResult
from ..models.company import CompanyProfile
from ..database.db import Database
from ..database.repository import Repository

def run_company_intelligence(company_name, stock_symbol=None, start_date=None, end_date=None, search_engine=None, extractor=None, persist=True):
    start_date=start_date or date.today()-timedelta(days=30); end_date=end_date or date.today(); company=company_name if (isinstance(company_name, CompanyProfile) or (hasattr(company_name, "name") and hasattr(company_name, "model_dump"))) else CompanySearch(allow_remote=True).identify(company_name)
    if stock_symbol: company.stock_symbol=stock_symbol
    queries=generate_queries(company.name, company.aliases, company.stock_symbol, company.industry); engine=search_engine or SearchEngine(); raw=engine.search(queries, company.name, start_date, end_date)
    extractor=extractor or ArticleExtractor(); articles=[]; warnings=[]
    for a in raw[:60]: articles.append(classify_article(clean_article(extractor.extract(str(a.url), company.name, a.headline, a.publisher, a.source_type, a.publication_date, a.summary))))
    groups, unique=group_duplicates(articles); analyses=[ArticleAnalyzer().analyze(a) for a in unique]
    if not raw: warnings.append("No RSS results were accessible. Configure a compliant search provider or add official RSS endpoints.")
    if any(not a.accessible_content for a in articles): warnings.append("Some sources provided only a headline/snippet or were inaccessible; they are not treated as full article evidence.")
    report=build_report(company, articles, analyses, warnings, start_date, end_date)
    result=ResearchResult(company=company, articles=articles, analyses=analyses, news_events=[{"event_id":g["event_id"],"urls":[str(x.url) for x in g["articles"]]} for g in groups], report=report, source_coverage=[{"source":"Google News RSS","status":"attempted"}], warnings=warnings)
    if persist:
        repository=Repository(Database())
        repository.save_research(result)
        repository.save_json(result)
    return result
