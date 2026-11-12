from pydantic import BaseModel, Field
from .company import CompanyProfile
from .article import Article, ArticleAnalysis

class CompanyIntelligenceReport(BaseModel):
    company_information: dict = Field(default_factory=dict)
    research_period: dict = Field(default_factory=dict)
    executive_summary: str = "Insufficient information."
    sections: dict[str, str] = Field(default_factory=dict)
    positive_developments: list[str] = Field(default_factory=list)
    negative_developments: list[str] = Field(default_factory=list)
    future_opportunities: list[str] = Field(default_factory=list)
    key_risks: list[str] = Field(default_factory=list)
    overall_business_outlook: str = "Insufficient information"
    sources: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

    def to_markdown(self) -> str:
        lines = [f"# Company Intelligence Report: {self.company_information.get('name', 'Unknown')}", "", "## Company Information", ""]
        lines += [f"- **{k.replace('_', ' ').title()}:** {v}" for k, v in self.company_information.items()]
        lines += ["", "## Executive Summary", "", self.executive_summary, ""]
        for title, body in self.sections.items(): lines += [f"## {title}", "", body or "No verified developments found.", ""]
        for title, values in (("Positive Developments", self.positive_developments), ("Negative Developments", self.negative_developments), ("Future Opportunities", self.future_opportunities), ("Key Risks to Monitor", self.key_risks)):
            lines += [f"## {title}", ""] + ([f"- {x}" for x in values] or ["- None identified from accessible evidence."]) + [""]
        lines += ["## Overall Business Outlook", "", f"**{self.overall_business_outlook}**", "", "## Sources and References", ""]
        lines += [f"- [{u}]({u})" for u in self.sources]
        return "\n".join(lines)

class ResearchResult(BaseModel):
    company: CompanyProfile
    articles: list[Article] = Field(default_factory=list)
    analyses: list[ArticleAnalysis] = Field(default_factory=list)
    news_events: list[dict] = Field(default_factory=list)
    report: CompanyIntelligenceReport
    source_coverage: list[dict] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
