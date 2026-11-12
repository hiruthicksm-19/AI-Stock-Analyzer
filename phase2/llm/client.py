import json, os
class GroqClient:
    def __init__(self, api_key=None, model=None):
        self.api_key=api_key or os.getenv("GROQ_API_KEY"); self.model=model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"); self.client=None
        if self.api_key:
            from groq import Groq
            self.client=Groq(api_key=self.api_key)
    def complete_json(self, system, payload):
        if not self.client: return None
        response=self.client.chat.completions.create(model=self.model, temperature=0.1, response_format={"type":"json_object"}, messages=[{"role":"system","content":system},{"role":"user","content":json.dumps(payload, default=str)}])
        return json.loads(response.choices[0].message.content)
