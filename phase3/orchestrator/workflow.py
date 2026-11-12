from .research_orchestrator import ResearchOrchestrator

def run_research(query: str, **kwargs):
    return ResearchOrchestrator().run(query, **kwargs)

