import json
from typing import Any, Literal
from pydantic import BaseModel, Field, field_validator

Assessment = Literal["Strong fundamentals", "Moderately strong fundamentals", "Mixed fundamentals", "Weak fundamentals", "Insufficient data"]

class ResearchReport(BaseModel):
    company_name: str
    assessment: Assessment
    company_overview: str
    financial_performance: str
    growth_analysis: str
    profitability_analysis: str
    financial_health: str
    shareholding_analysis: str
    valuation_analysis: str
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    risk_assessment: list[str] = Field(default_factory=list)
    conclusion: str
    evidence_notes: list[str] = Field(default_factory=list)

    @field_validator(
        "company_overview", "financial_performance", "growth_analysis",
        "profitability_analysis", "financial_health", "shareholding_analysis",
        "valuation_analysis", "conclusion", mode="before",
    )
    @classmethod
    def normalize_section(cls, value: Any) -> str:
        """Accept LLM prose or structured analysis and preserve structured evidence."""
        if isinstance(value, str):
            return value
        return json.dumps(value, ensure_ascii=False, indent=2, default=str)

    def to_markdown(self) -> str:
        sections = [("Company Overview", self.company_overview), ("Financial Performance", self.financial_performance), ("Growth Analysis", self.growth_analysis), ("Profitability Analysis", self.profitability_analysis), ("Financial Health", self.financial_health), ("Shareholding Analysis", self.shareholding_analysis), ("Valuation Analysis", self.valuation_analysis)]
        out = [f"# AI Stock Research Report: {self.company_name}", f"\n## Overall Fundamental Assessment\n**{self.assessment}**\n"]
        for title, body in sections: out += [f"## {title}\n{body}\n"]
        out += ["## Strengths\n" + "\n".join(f"- {x}" for x in self.strengths), "\n## Weaknesses\n" + "\n".join(f"- {x}" for x in self.weaknesses), "\n## Risk Assessment\n" + "\n".join(f"- {x}" for x in self.risk_assessment), f"\n## Final Research Conclusion\n{self.conclusion}"]
        return "\n".join(out)

