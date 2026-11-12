from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field, ConfigDict

Stance = Literal["BUY CANDIDATE", "WATCH / WAIT", "AVOID FOR NOW", "INSUFFICIENT DATA"]

class CompanySummary(BaseModel):
    name: str
    symbol: str | None = None
    exchange: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap: float | None = None
    current_price: float | None = None
    currency: str | None = "INR"
    source_url: str | None = None

class Evidence(BaseModel):
    id: str
    kind: Literal["financial", "news"]
    label: str
    source_url: str | None = None
    period: str | None = None

class NewsEvent(BaseModel):
    model_config = ConfigDict(extra="allow")
    event_id: str
    headline: str
    publisher: str | None = None
    publication_date: str | None = None
    source_url: str | None = None
    category: str = "Other"
    summary: str
    business_impact: str = "Unknown"
    revenue_effect: str = "Unknown"
    profitability_effect: str = "Unknown"
    capital_or_debt_effect: str = "Unknown"
    risk_or_opportunity: str = "Unknown"
    time_horizon: str = "Unknown"
    reliability: str = "medium"
    verification_status: str = "Unverified"
    evidence_id: str | None = None

class InvestmentPayload(BaseModel):
    company: CompanySummary
    financial_analysis: dict[str, Any] = Field(default_factory=dict)
    business_intelligence: dict[str, Any] = Field(default_factory=dict)
    evidence: dict[str, list[Evidence]] = Field(default_factory=lambda: {"financial_sources": [], "news_sources": []})
    metadata: dict[str, Any] = Field(default_factory=dict)

class InvestmentReport(BaseModel):
    stance: Stance = "INSUFFICIENT DATA"
    confidence: str = "low"
    company_overview: str = ""
    executive_summary: str = ""
    fundamental_analysis: str = ""
    business_intelligence_analysis: str = ""
    positive_factors: list[str] = Field(default_factory=list)
    negative_factors: list[str] = Field(default_factory=list)
    valuation_analysis: str = ""
    risk_analysis: list[str] = Field(default_factory=list)
    combined_evidence_analysis: str = ""
    future_outlook: str = ""
    supporting_reasons: list[str] = Field(default_factory=list)
    opposing_reasons: list[str] = Field(default_factory=list)
    conditions_to_reconsider: list[str] = Field(default_factory=list)
    monitor: list[str] = Field(default_factory=list)
    conclusion: str = "Insufficient verified data for a combined assessment."
    evidence_ids: list[str] = Field(default_factory=list)
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

