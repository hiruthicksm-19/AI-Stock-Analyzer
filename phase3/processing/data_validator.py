from dataclasses import dataclass, field
from typing import Any

@dataclass
class ValidationResult:
    valid: bool
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

def validate_financial(raw: dict) -> ValidationResult:
    dataset = raw.get("dataset", raw)
    warnings = list(dataset.get("warnings", [])) if isinstance(dataset, dict) else ["Financial dataset is not a mapping."]
    errors = [] if isinstance(dataset, dict) and dataset.get("company") else ["Financial dataset has no company profile."]
    return ValidationResult(not errors, warnings, errors)

def validate_news(raw: dict) -> ValidationResult:
    errors = [] if isinstance(raw, dict) and raw.get("company") else ["News result has no company profile."]
    warnings = list(raw.get("warnings", [])) if isinstance(raw, dict) else ["News result is not a mapping."]
    return ValidationResult(not errors, warnings, errors)

