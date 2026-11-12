from datetime import datetime, timezone
from typing import Any
from pydantic import BaseModel, Field, ConfigDict

class CompanyProfile(BaseModel):
    name: str
    sector: str | None = None
    description: str | None = None
    source_url: str
    market_cap: float | None = None
    current_price: float | None = None
    face_value: float | None = None
    exchange: str | None = None
    retrieved_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class PeriodRecord(BaseModel):
    model_config = ConfigDict(extra="allow")
    period: str
    values: dict[str, float | None] = Field(default_factory=dict)
    raw_values: dict[str, str | None] = Field(default_factory=dict)
    unit: str | None = None

class FinancialDataset(BaseModel):
    company: CompanyProfile
    profit_loss_annual: list[PeriodRecord] = Field(default_factory=list)
    profit_loss_quarterly: list[PeriodRecord] = Field(default_factory=list)
    balance_sheet_annual: list[PeriodRecord] = Field(default_factory=list)
    cash_flow_annual: list[PeriodRecord] = Field(default_factory=list)
    ratios: dict[str, float | None] = Field(default_factory=dict)
    shareholding: list[PeriodRecord] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    retrieval_errors: list[str] = Field(default_factory=list)

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")

