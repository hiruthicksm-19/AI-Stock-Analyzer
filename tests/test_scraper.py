from stock_research_agent.scraper.parsers import parse_number, parse_financial_table

HTML = '''<table><thead><tr><th> </th><th>Mar 2023</th><th>Mar 2024</th></tr></thead><tbody><tr><td>Sales</td><td>1,000</td><td>1,200</td></tr><tr><td>Net Profit</td><td>100</td><td>-</td></tr></tbody></table>'''

def test_numeric_conversion_and_missing_values():
    assert parse_number("₹1,234.50") == 1234.5
    assert parse_number("-") is None
    assert parse_number("12.5%") == .125

def test_financial_table_parser_preserves_periods_and_raw_values():
    rows = parse_financial_table(HTML)
    assert rows[0]["label"] == "Sales"
    assert rows[0]["values"]["Mar 2024"] == 1200
    assert rows[1]["values"]["Mar 2024"] is None
    assert rows[1]["raw_values"]["Mar 2024"] == "-"

