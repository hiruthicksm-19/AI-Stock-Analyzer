from pydantic import BaseModel, Field
class NewsEvent(BaseModel):
    event_id: str
    headline: str
    article_urls: list[str] = Field(default_factory=list)
    original_url: str | None = None
    independent_coverage_urls: list[str] = Field(default_factory=list)
    syndicated_urls: list[str] = Field(default_factory=list)
