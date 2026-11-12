from pydantic import BaseModel, Field

class CompanyProfile(BaseModel):
    name: str
    stock_symbol: str | None = None
    exchange: str | None = None
    official_website: str | None = None
    industry: str | None = None
    sector: str | None = None
    aliases: list[str] = Field(default_factory=list)
    confidence: float = 0.0
    verified: bool = False
