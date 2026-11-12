import pandas as pd
def chart_frames(result):
    rows=[{"date":a.publication_date.date() if a.publication_date else None,"category":c.value,"publisher":a.publisher} for a in result.articles for c in (a.categories or [])]
    return pd.DataFrame(rows)
