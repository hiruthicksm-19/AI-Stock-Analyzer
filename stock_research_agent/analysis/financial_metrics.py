from math import isfinite
from ..models.financial_data import FinancialDataset

def _value(row, *names):
    for name in names:
        if name in row.values and row.values[name] is not None: return row.values[name]
    return None

def growth(values: list[float | None]) -> list[float | None]:
    out = [None]
    for old, new in zip(values, values[1:]): out.append(None if old in (None, 0) or new is None else (new / old) - 1)
    return out

def cagr(start: float | None, end: float | None, years: int) -> float | None:
    if start in (None, 0) or end is None or years <= 0 or start < 0 or end < 0: return None
    return (end / start) ** (1 / years) - 1

def calculate_metrics(data: FinancialDataset) -> dict:
    annual = sorted(data.profit_loss_annual, key=lambda x: x.period)
    revenue = [_value(x, "sales", "revenue", "sales / revenue") for x in annual]
    profit = [_value(x, "net profit", "profit after tax", "pat") for x in annual]
    latest = annual[-1] if annual else None
    ratios = dict(data.ratios)
    if latest:
        sales = _value(latest, "sales", "revenue", "sales / revenue")
        net = _value(latest, "net profit", "profit after tax", "pat")
        ratios.setdefault("net profit margin", None if sales in (None, 0) or net is None else net / sales)
    bs = sorted(data.balance_sheet_annual, key=lambda x: x.period)
    borrowings = [_value(x, "borrowings", "total borrowings") for x in bs]
    cash = sorted(data.cash_flow_annual, key=lambda x: x.period)
    ocf = [_value(x, "cash from operating activity", "cash from operating activities", "cash from operating") for x in cash]
    return {
        "annual_periods": [x.period for x in annual],
        "revenue_growth_yoy": growth(revenue), "net_profit_growth_yoy": growth(profit),
        "revenue_cagr_3y": cagr(revenue[-4], revenue[-1], 3) if len(revenue) >= 4 else None,
        "revenue_cagr_5y": cagr(revenue[-6], revenue[-1], 5) if len(revenue) >= 6 else None,
        "net_profit_cagr_3y": cagr(profit[-4], profit[-1], 3) if len(profit) >= 4 else None,
        "net_profit_cagr_5y": cagr(profit[-6], profit[-1], 5) if len(profit) >= 6 else None,
        "quarterly_revenue_growth": growth([_value(x, "sales", "revenue") for x in sorted(data.profit_loss_quarterly, key=lambda x: x.period)]),
        "quarterly_net_profit_growth": growth([_value(x, "net profit", "profit after tax") for x in sorted(data.profit_loss_quarterly, key=lambda x: x.period)]),
        "ratios": ratios,
        "borrowings": borrowings, "operating_cash_flow": ocf,
        "warnings": (["Revenue CAGR is not meaningful with insufficient, zero, or negative starting data."] if len(revenue) < 4 or (revenue and (revenue[-4] is None or revenue[-4] <= 0)) else []),
    }

