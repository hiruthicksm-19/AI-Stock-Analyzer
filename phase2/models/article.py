from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, HttpUrl

class SourceType(str, Enum):
    OFFICIAL_EXCHANGE = "official_exchange_disclosure"
    GOVERNMENT = "government_source"
    COMPANY = "company_press_release"
    FINANCIAL_NEWS = "financial_news"
    CREDIT_RATING = "credit_rating_report"
    INDUSTRY = "industry_report"
    OTHER = "other"

class ArticleCategory(str, Enum):
    EXPANSION = "Business Expansion"
    ORDERS = "New Orders and Contracts"
    FINANCIAL = "Financial Developments"
    PRODUCT = "Product and Technology Developments"
    MANAGEMENT = "Management and Director Changes"
    LEGAL = "Legal and Regulatory Issues"
    CREDIT = "Credit and Financial Risk"
    INDUSTRY = "Industry and Competitor Developments"
    GOVERNANCE = "Corporate Governance"

class Article(BaseModel):
    headline: str
    url: HttpUrl
    publisher: str
    author: str | None = None
    publication_date: datetime | None = None
    retrieved_at: datetime
    content: str = ""
    summary: str = ""
    company_name: str
    entities: list[str] = Field(default_factory=list)
    source_type: SourceType = SourceType.OTHER
    accessible_content: bool = True
    retrieval_error: str | None = None
    categories: list[ArticleCategory] = Field(default_factory=list)
    event_id: str | None = None

class ArticleAnalysis(BaseModel):
    article_url: str
    what_happened: str
    why_it_matters: str
    business_impact: str
    affected_operations: list[str] = Field(default_factory=list)
    revenue_effect: str = "Unknown"
    profitability_effect: str = "Unknown"
    capital_or_debt_effect: str = "Unknown"
    competitive_effect: str = "Unknown"
    time_horizon: str = "Unknown"
    evidence: list[str] = Field(default_factory=list)
    uncertainties: list[str] = Field(default_factory=list)
    reliability: str = "medium"
    sentiment: str = "mixed"
    confidence: float = 0.5
