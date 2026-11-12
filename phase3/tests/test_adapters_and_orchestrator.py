from types import SimpleNamespace
from phase3.adapters.phase1_adapter import Phase1Adapter
from phase3.adapters.phase2_adapter import Phase2Adapter
from phase3.orchestrator.research_orchestrator import ResearchOrchestrator

class FakeAgent:
    def run(self, query, selected_url=None):
        return {"dataset": SimpleNamespace(as_dict=lambda: {"company":{"name":"Acme","source_url":"u"},"profit_loss_annual":[]}), "metrics": {}, "report": None}

class FakeNews:
    def __init__(self): self.company=SimpleNamespace(name="Acme", stock_symbol="ACME"); self.articles=[]; self.analyses=[]; self.warnings=[]
    def model_dump(self, mode="json"): return {"company":{"name":"Acme","stock_symbol":"ACME"},"articles":[],"analyses":[],"warnings":[]}

def test_adapters_keep_public_contracts():
    assert "dataset" in Phase1Adapter(FakeAgent()).run("Acme")
    assert Phase2Adapter(lambda *args, **kwargs: FakeNews()).raw_dict(FakeNews())["company"]["name"] == "Acme"

def test_partial_failure_is_explicit():
    class Broken:
        def run(self, *args, **kwargs): raise RuntimeError("offline")
    o = ResearchOrchestrator(phase1=Phase1Adapter(FakeAgent()), phase2=Phase2Adapter(Broken()))
    result = o.run("Acme")
    assert result.partial is True
    assert any("Phase 2" in e for e in result.errors)

