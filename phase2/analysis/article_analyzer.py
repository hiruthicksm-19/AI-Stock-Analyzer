from ..models.article import ArticleAnalysis
from .business_impact import heuristic_impact
class ArticleAnalyzer:
    def __init__(self, llm=None): self.llm=llm
    def analyze(self, article):
        if self.llm:
            try: return self.llm.analyze_article(article)
            except Exception: pass
        return ArticleAnalysis(article_url=str(article.url), **heuristic_impact(article))
