"""Compliant crawler adapter with Crawl4AI optional and requests fallback."""
import asyncio
class Crawler:
    def __init__(self, timeout=20): self.timeout=timeout
    def fetch(self, url: str) -> str:
        try:
            from crawl4ai import AsyncWebCrawler
            async def run():
                async with AsyncWebCrawler() as crawler:
                    result=await crawler.arun(url=url)
                    return getattr(result, "html", "") or getattr(result, "cleaned_html", "")
            return asyncio.run(run())
        except Exception:
            import requests
            response=requests.get(url, timeout=self.timeout, headers={"User-Agent":"Phase2-Company-Intelligence/1.0"}); response.raise_for_status(); return response.text
