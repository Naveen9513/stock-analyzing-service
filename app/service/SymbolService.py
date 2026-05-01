class SymbolService:
    def __init__(self):
        pass

    def get_annual_summary(self, symbol: str, year: int):

        # TODO: validation layer
        # TODO: check if data exist in local db
        # TODO: if data exist in local db => return 
        # TODO: if not fetch from external API and return
        return {
        "symbol": symbol.upper(),
        "year": year,
        "high": 1500.0,
        "low": 100.0,
        "volume": 1000000
    }