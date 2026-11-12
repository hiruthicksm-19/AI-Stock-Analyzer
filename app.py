import os, json
from pathlib import Path
import streamlit as st
import plotly.express as px
from dotenv import load_dotenv
from groq import Groq
from stock_research_agent.agent import StockResearchAgent
from stock_research_agent.llm import Analyst

load_dotenv()
st.set_page_config(page_title="AI Stock Research Analyst", layout="wide")
st.title("AI Stock Research Analyst")
st.caption("Phase 1: fundamental analysis from publicly accessible Screener.in data. Not investment advice.")
if not os.getenv("GROQ_API_KEY"):
    st.warning("No GROQ_API_KEY is configured. Data and deterministic metrics will still load; configure .env to generate the LLM research narrative.")

def build_agent():
    client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
    return StockResearchAgent(analyst=Analyst(client, os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")))

query = st.text_input("Indian listed company", placeholder="e.g. Infosys")
if st.button("Analyse Company", type="primary") and query:
    with st.spinner("Searching, retrieving and validating Screener data..."):
        try:
            result = build_agent().run(query)
            if "matches" in result:
                st.session_state.matches = result["matches"]
                st.info("Multiple companies matched. Select the exact company below.")
            else: st.session_state.result = result
        except Exception as exc: st.error(str(exc))

if st.session_state.get("matches"):
    match = st.selectbox("Confirm company", st.session_state.matches, format_func=lambda m: f"{m.name} — {m.url}")
    if st.button("Confirm and retrieve"):
        with st.spinner("Retrieving financial data..."):
            try: st.session_state.result = build_agent().run(query, match.url); st.session_state.matches = None
            except Exception as exc: st.error(str(exc))

result = st.session_state.get("result")
if result:
    data, metrics, report = result["dataset"], result["metrics"], result["report"]
    c = data.company
    st.subheader(c.name); st.write(f"Sector: {c.sector or 'Unavailable'} · Source: [{c.source_url}]({c.source_url})")
    st.caption(f"Retrieved: {c.retrieved_at}")
    st.metric("Assessment", report.assessment)
    tabs = st.tabs(["Dashboard", "AI Report", "Data Explorer"])
    with tabs[0]:
        rows = [{"period": r.period, "revenue": next((v for k,v in r.values.items() if k in ('sales','revenue','sales / revenue')), None), "net profit": next((v for k,v in r.values.items() if k in ('net profit','profit after tax','pat')), None)} for r in data.profit_loss_annual]
        if rows: st.plotly_chart(px.line(rows, x="period", y=["revenue", "net profit"], markers=True, title="Annual revenue and net profit"), use_container_width=True)
        st.json(metrics)
    with tabs[1]: st.markdown(report.to_markdown())
    with tabs[2]:
        payload = json.dumps(data.as_dict(), indent=2, default=str)
        st.download_button("Download JSON", payload, file_name=f"{c.name.replace(' ', '_')}.json", mime="application/json")
        st.download_button("Download Markdown report", report.to_markdown(), file_name=f"{c.name.replace(' ', '_')}_report.md", mime="text/markdown")
        st.json(data.as_dict())

