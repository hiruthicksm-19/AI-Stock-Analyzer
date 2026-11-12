import json, sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, str(Path(__file__).parents[1]))
from phase3.orchestrator.research_orchestrator import ResearchOrchestrator

st.set_page_config(page_title="AI Stock Research & Investment Analyst", layout="wide")
st.title("AI Stock Research & Investment Analyst")
st.caption("Phase 3 combines validated Phase 1 fundamentals and Phase 2 business intelligence. It is research support, not financial advice.")
query = st.text_input("Company name or symbol", placeholder="e.g. Infosys")
days = st.selectbox("Research period", [30, 90, 182, 365], index=1, format_func=lambda x: f"Last {x} days")
if st.button("Analyse Stock", type="primary") and query:
    with st.status("Running unified research workflow", expanded=True) as status:
        result = ResearchOrchestrator().run(query, research_days=days)
        st.session_state.phase3_result = result
        status.update(label="Workflow finished", state="complete" if not result.errors else "error")
result = st.session_state.get("phase3_result")
if result:
    if result.errors: st.warning(" | ".join(result.errors))
    for stage in result.stages: st.write(f"**{stage.name}** — {stage.status} {stage.message}")
    if result.report:
        report = result.report
        st.subheader(report.stance); st.metric("Confidence", report.confidence)
        st.write(report.executive_summary); st.write(report.conclusion)
        for title, body in [("Company Overview", report.company_overview),("Fundamental Analysis", report.fundamental_analysis),("Business Intelligence", report.business_intelligence_analysis),("Valuation", report.valuation_analysis),("Combined Evidence", report.combined_evidence_analysis),("Future Outlook", report.future_outlook)]:
            with st.expander(title): st.write(body)
        c1,c2 = st.columns(2)
        with c1: st.markdown("**Positive factors**"); st.write(report.positive_factors)
        with c2: st.markdown("**Risks / negative factors**"); st.write(report.negative_factors + report.risk_analysis)
    with st.expander("Optimized JSON sent to LLM"): st.json(result.optimized_payload)
    with st.expander("Original Phase 1 JSON"): st.json(result.financial_raw)
    with st.expander("Original Phase 2 JSON"): st.json(result.news_raw)
    st.download_button("Download optimized JSON", json.dumps(result.optimized_payload, indent=2, default=str), "optimized_payload.json", "application/json")
    if result.report: st.download_button("Download report JSON", result.report.model_dump_json(indent=2), "investment_report.json", "application/json")

