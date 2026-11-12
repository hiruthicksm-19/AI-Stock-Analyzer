from dataclasses import dataclass, asdict
from datetime import datetime, timezone

@dataclass
class TokenUsage:
    model_name: str
    estimated_input_tokens: int
    actual_input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None
    request_timestamp: str = ""
    selected_news_events: int = 0
    excluded_news_events: int = 0
    payload_size_bytes: int = 0
    analysis_status: str = "not_started"
    def __post_init__(self):
        if not self.request_timestamp: self.request_timestamp = datetime.now(timezone.utc).isoformat()
    def as_dict(self): return asdict(self)

