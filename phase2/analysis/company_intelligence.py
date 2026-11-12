from ..models.report import CompanyIntelligenceReport
def build_report(company, articles, analyses, warnings=None, start_date=None, end_date=None):
    sections={}
    for title in ["Recent Company News","Business Expansion Analysis","Orders and Contracts","Financial and Strategic Developments","Management and Governance Developments","Legal and Regulatory Risk","Credit and Financial Risk","Industry and Competitor Analysis"]:
        rows=[f"- {a.what_happened} (reliability: {a.reliability}; source: {a.article_url})" for a in analyses[:10]]
        sections[title]="\n".join(rows) if rows else "No verified developments were available for this section."
    positives=[a.business_impact for a in analyses if a.sentiment=="positive"]; negatives=[a.business_impact for a in analyses if a.sentiment=="negative"]
    outlook="Insufficient information" if not analyses else "Mixed business outlook"
    return CompanyIntelligenceReport(company_information=company.model_dump(), research_period={"start":str(start_date or ""),"end":str(end_date or "")}, executive_summary=f"Collected {len(articles)} accessible or headline-level articles and grouped them into {len({a.event_id for a in articles if a.event_id})} news events. This is business intelligence, not stock-price prediction or investment advice.", sections=sections, positive_developments=positives[:10], negative_developments=negatives[:10], key_risks=[u for a in analyses for u in a.uncertainties][:10], overall_business_outlook=outlook, sources=[str(a.url) for a in articles], warnings=warnings or [])
