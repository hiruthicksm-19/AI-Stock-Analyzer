def generate_queries(company_name: str, aliases=None, symbol=None, industry=None) -> list[str]:
    terms = [company_name, *(aliases or [])]
    topics = ["latest news", "business expansion", "new orders", "new contracts", "acquisition", "financial performance", "management changes", "regulatory issues", "credit rating", "international expansion"]
    queries = [f'"{term}" {topic}' for term in terms for topic in topics]
    if symbol: queries += [f"{symbol} company announcement", f"{symbol} NSE BSE filing"]
    if industry: queries.append(f"{industry} industry developments India")
    return list(dict.fromkeys(queries))
