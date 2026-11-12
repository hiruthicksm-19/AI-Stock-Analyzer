from ..models.company import CompanyProfile

KNOWN_COMPANIES = [
    CompanyProfile(name="Infosys Limited", stock_symbol="INFY", exchange="NSE/BSE", official_website="https://www.infosys.com", industry="Information Technology", sector="IT Services", aliases=["Infosys", "Infosys Ltd"], confidence=1, verified=True),
    CompanyProfile(name="Tata Consultancy Services Limited", stock_symbol="TCS", exchange="NSE/BSE", official_website="https://www.tcs.com", industry="Information Technology", sector="IT Services", aliases=["TCS", "Tata Consultancy Services"], confidence=1, verified=True),
    CompanyProfile(name="Reliance Industries Limited", stock_symbol="RELIANCE", exchange="NSE/BSE", official_website="https://www.ril.com", industry="Diversified", sector="Conglomerate", aliases=["Reliance", "RIL"], confidence=1, verified=True),
    CompanyProfile(name="Tech Mahindra Limited", stock_symbol="TECHM", exchange="NSE/BSE", official_website="https://www.techmahindra.com", industry="Information Technology", sector="IT Services", aliases=["Tech Mahindra", "Tech Mahindra Ltd"], confidence=1, verified=True),
]
