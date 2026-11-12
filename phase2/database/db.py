import sqlite3
from pathlib import Path
class Database:
    def __init__(self, path=None):
        self.path=Path(path or Path(__file__).parents[1]/"storage"/"phase2.sqlite3"); self.path.parent.mkdir(parents=True, exist_ok=True); self.init()
    def connect(self): return sqlite3.connect(self.path)
    def init(self):
        with self.connect() as c:
            c.executescript("""CREATE TABLE IF NOT EXISTS companies(id INTEGER PRIMARY KEY,name TEXT NOT NULL,stock_symbol TEXT,exchange TEXT,profile_json TEXT); CREATE TABLE IF NOT EXISTS articles(id INTEGER PRIMARY KEY,company_id INTEGER,url TEXT UNIQUE,headline TEXT,publisher TEXT,publication_date TEXT,retrieved_at TEXT,content TEXT,summary TEXT,source_type TEXT,categories TEXT,event_id TEXT,analysis_json TEXT); CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY,company_id INTEGER,created_at TEXT,report_json TEXT);""")
