import json, os
from phase3.utils.config import Phase3Config, REQUIRED_GROQ_MODEL

class Phase3LLMClient:
    def __init__(self, api_key=None, model=None, client=None):
        config = Phase3Config(); self.model = REQUIRED_GROQ_MODEL; self.client = client
        if self.client is None and (api_key or config.groq_api_key):
            from groq import Groq
            self.client = Groq(api_key=api_key or config.groq_api_key)
    def complete_json(self, system: str, payload: dict, max_tokens: int = 3500):
        if not self.client: return None, None
        response = self.client.chat.completions.create(model=self.model, temperature=0.1, max_tokens=max_tokens, response_format={"type":"json_object"}, messages=[{"role":"system","content":system},{"role":"user","content":json.dumps(payload, ensure_ascii=False, default=str, separators=(",", ":"))}])
        usage = getattr(response, "usage", None)
        return json.loads(response.choices[0].message.content), usage

