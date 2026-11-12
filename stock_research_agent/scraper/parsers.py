import re
from bs4 import BeautifulSoup

MISSING = {"", "-", "—", "–", "nan", "na", "n/a", "not available"}

def parse_number(value: object) -> float | None:
    if value is None: return None
    text = str(value).strip().replace(",", "").replace("₹", "")
    if text.lower() in MISSING: return None
    multiplier = 1
    if text.endswith("%"): text, multiplier = text[:-1], 0.01
    try: return float(re.sub(r"[^0-9.\-]", "", text)) * multiplier
    except ValueError: return None

def parse_financial_table(html: str, table_id: str | None = None) -> list[dict[str, object]]:
    soup = BeautifulSoup(html, "lxml")
    table = soup.find("table", id=table_id) if table_id else soup.find("table")
    if not table: return []
    headers = [x.get_text(" ", strip=True) for x in table.select("thead th")]
    if not headers:
        first = table.find("tr")
        headers = [x.get_text(" ", strip=True) for x in first.find_all(["th", "td"])] if first else []
    records = []
    for tr in table.select("tbody tr") or table.select("tr")[1:]:
        cells = [x.get_text(" ", strip=True) for x in tr.find_all(["th", "td"])]
        if len(cells) < 2: continue
        label = cells[0]
        values = {headers[i] if i < len(headers) else f"period_{i}": parse_number(v) for i, v in enumerate(cells[1:], 1)}
        records.append({"label": label, "values": values, "raw_values": dict(zip(headers[1:], cells[1:]))})
    return records

