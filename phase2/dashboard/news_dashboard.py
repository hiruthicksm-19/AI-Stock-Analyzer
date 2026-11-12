def render_news(st, result):
    for article, analysis in zip(result.articles, result.analyses):
        with st.expander(article.headline):
            st.write(f"{article.publisher} · {article.publication_date or 'Publication date unavailable'}")
            st.write(analysis.business_impact); st.markdown(f"[Open original source]({article.url})")
