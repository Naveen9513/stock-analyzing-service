class SymbolRepository:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def get_aggregated_data(self, symbol: str, year: int):

        # TODO: load from database once setup
        return {
        "symbol": symbol.upper(),
        "year": year,
        "high": 1400.0,
        "low": 100.0,
        "volume": 1000000}