import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

REQUIRED_GROQ_MODEL = "openai/gpt-oss-120b"

@dataclass(frozen=True)
class Phase3Config:
    groq_api_key: str | None = os.getenv("GROQ_API_KEY")
    # Phase 3 intentionally supports one model only.
    groq_model: str = REQUIRED_GROQ_MODEL
    max_input_tokens: int = int(os.getenv("MAX_INPUT_TOKENS", "12000"))
    max_news_events: int = int(os.getenv("MAX_NEWS_EVENTS", "15"))
    max_summary_length: int = int(os.getenv("MAX_SUMMARY_LENGTH", "500"))
    max_financial_observations: int = int(os.getenv("MAX_FINANCIAL_OBSERVATIONS", "10"))
    system_prompt_reserve: int = int(os.getenv("SYSTEM_PROMPT_RESERVE", "1500"))
    output_token_reserve: int = int(os.getenv("OUTPUT_TOKEN_RESERVE", "3500"))

