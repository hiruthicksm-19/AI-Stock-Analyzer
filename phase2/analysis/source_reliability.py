RANK={"official_exchange_disclosure":"highest","government_source":"high","company_press_release":"high","credit_rating_report":"high","financial_news":"medium","industry_report":"medium","other":"low"}
def reliability(article):
    key=article.source_type.value if hasattr(article.source_type, "value") else str(article.source_type)
    return RANK.get(key, "low")
