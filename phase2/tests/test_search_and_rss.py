from phase2.search.query_generator import generate_queries
from phase2.scraper.rss_reader import parse_feed
from phase2.search.search_engine import SearchEngine
def test_queries_cover_business_topics():
    qs=generate_queries("Infosys", ["INFY"], "INFY", "IT")
    assert any("new contracts" in q for q in qs); assert any("INFY NSE BSE" in q for q in qs)
def test_rss_parsing_preserves_missing_date():
    rows=parse_feed('<rss version="2.0"><channel><item><title>Headline</title><link>https://example.com/a</link></item></channel></rss>')
    assert rows[0]["headline"] == "Headline" and rows[0]["publication_date"] is None

def test_search_engine_maps_feedparser_fields(monkeypatch):
    class FakeFeed:
        entries=[{"title":"INFY wins contract", "link":"https://example.com/news", "summary":"A contract was announced."}]
    monkeypatch.setattr("phase2.search.search_engine.feedparser", type("FakeParser", (), {"parse": staticmethod(lambda url: FakeFeed())}))
    rows=SearchEngine().search_rss("INFY contract", "Infosys")
    assert len(rows)==1 and rows[0].headline == "INFY wins contract"

def test_search_filters_unrelated_and_noise_results(monkeypatch):
    class FakeParser:
        @staticmethod
        def parse(url):
            return type("Feed", (), {"entries":[{"title":"ICICI Bank signs trade agreement", "link":"https://example.com/1", "summary":"Business agreement"}, {"title":"Ventive Hospitality results", "link":"https://example.com/2", "summary":"Unrelated company"}, {"title":"ICICI Bank stock forecast", "link":"https://example.com/3", "summary":"Analyst predictions"}]})()
    monkeypatch.setattr("phase2.search.search_engine.feedparser", FakeParser)
    rows=SearchEngine().search(["ICICI latest news"], "ICICI Bank")
    assert len(rows)==1 and rows[0].headline.startswith("ICICI Bank signs")
