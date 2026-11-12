from datetime import datetime, timezone
from phase2.models.article import Article, SourceType, ArticleCategory
from phase2.processing.deduplication import canonicalize_url, group_duplicates
from phase2.processing.article_classifier import classify_article
def article(headline, url): return Article(headline=headline,url=url,publisher="Test",retrieved_at=datetime.now(timezone.utc),company_name="Infosys")
def test_url_normalization_and_duplicate_grouping():
    assert canonicalize_url("HTTPS://Example.com/a/?utm_source=x")=="https://example.com/a"
    groups, unique=group_duplicates([article("Infosys announces new plant", "https://example.com/a"), article("Infosys announces new plant", "https://other.example/b")])
    assert len(groups)==1 and len(unique)==1
def test_multi_label_classification():
    a=article("Company wins new contract and appoints CFO", "https://example.com/a"); a=classify_article(a)
    assert ArticleCategory.ORDERS in a.categories and ArticleCategory.MANAGEMENT in a.categories
