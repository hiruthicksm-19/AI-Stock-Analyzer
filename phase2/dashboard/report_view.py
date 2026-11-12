def render_report(st, result):
    st.markdown(result.report.to_markdown())
