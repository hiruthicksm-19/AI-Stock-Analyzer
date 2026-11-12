from dataclasses import dataclass, field
from typing import Any

@dataclass
class StageResult:
    name: str
    status: str = "pending"
    message: str = ""
    data: Any = None

@dataclass
class WorkflowResult:
    query: str
    stages: list[StageResult] = field(default_factory=list)
    financial_raw: dict = field(default_factory=dict)
    news_raw: dict = field(default_factory=dict)
    optimized_payload: dict = field(default_factory=dict)
    report: Any = None
    errors: list[str] = field(default_factory=list)
    partial: bool = False

