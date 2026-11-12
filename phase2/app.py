import json, os, sys
from datetime import date, timedelta
from pathlib import Path
import streamlit as st
import plotly.express as px
import pandas as pd
sys.path.insert(0, str(Path(__file__).parents[1]))
from phase2.agent.intelligence_agent import run_company_intelligence
from phase2.company.company_search import CompanySearch, AmbiguousCompanyError
from phase2.dashboard.charts import chart_frames

st.set_page_config(page_title="AI Company Intelligence Agent", layout="wide")
st.title("AI Company Intelligence Agent")
st.caption("Phase 2: evidence-based company news and business intelligence. Not stock-price prediction or investment advice.")
query=st.text_input("Indian listed company", placeholder="e.g. Infosys")
period=st.selectbox("Research period", ["Last 7 days","Last 30 days","Last 90 days","Last 6 months","Last 1 year"], index=1)
days={"Last 7 days":7,"Last 30 days":30,"Last 90 days":90,"Last 6 months":182,"Last 1 year":365}[period]
if st.button("Analyse Company", type="primary") and query:
    try:
        matches=CompanySearch(allow_remote=True).find(query)
        if len(matches)>1: st.session_state.matches=matches
        else: st.session_state.result=run_company_intelligence(query, start_date=date.today()-timedelta(days=days), persist=True)
    except Exception as exc: st.error(str(exc))
if st.session_state.get("matches"):
    selected=st.selectbox("Confirm company", st.session_state.matches, format_func=lambda x:f"{x.name} — {x.stock_symbol}")
    if st.button("Confirm and research"):
        st.session_state.result=run_company_intelligence(selected, start_date=date.today()-timedelta(days=days), persist=True); st.session_state.matches=None
result=st.session_state.get("result")
if result:
    st.subheader(result.company.name); st.write(f"{result.company.stock_symbol or 'Symbol unavailable'} · {result.company.exchange or 'Exchange unavailable'} · {result.company.sector or 'Sector unavailable'}")
    if not result.company.verified:
        st.warning("This company was accepted as an unverified search profile. Confirm the identity, symbol, exchange and official website before relying on the results.")
    c1,c2,c3=st.columns(3); c1.metric("Articles",len(result.articles)); c2.metric("Unique events",len(result.news_events)); c3.metric("Outlook",result.report.overall_business_outlook)
    if result.warnings: st.warning(" ".join(result.warnings))
    tabs=st.tabs(["News Feed","Business Intelligence","Dashboard","Downloads"])
    with tabs[0]:
        for article in result.articles:
            st.markdown(f"### [{article.headline}]({article.url})"); st.caption(f"{article.publisher} · {article.publication_date or 'Publication date unavailable'} · {', '.join(x.value for x in article.categories)}")
            st.write(article.summary or "No article body was accessible; headline/snippet only.")
    with tabs[1]: st.markdown(result.report.to_markdown())
    with tabs[2]:
        frame=chart_frames(result)
        if not frame.empty:
            st.plotly_chart(px.histogram(frame, x="category", title="News category distribution"), use_container_width=True)
            st.plotly_chart(px.histogram(frame, x="publisher", title="Source distribution"), use_container_width=True)
    with tabs[3]:
        payload=json.dumps(result.model_dump(), indent=2, default=str); st.download_button("Download article metadata JSON", payload, file_name="company_intelligence.json", mime="application/json"); st.download_button("Download Markdown report", result.report.to_markdown(), file_name="company_intelligence.md", mime="text/markdown")
        csv=pd.DataFrame([{"headline":a.headline,"url":str(a.url),"publisher":a.publisher,"publication_date":a.publication_date,"categories":", ".join(x.value for x in a.categories),"event_id":a.event_id} for a in result.articles]).to_csv(index=False)
        st.download_button("Download article dataset CSV", csv, file_name="article_analysis.csv", mime="text/csv")
