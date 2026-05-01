from app.repository.SymbolRepository import SymbolRepository

class SymbolService:
    def __init__(self, symbolRepository: SymbolRepository):
        self.symbolRepository = symbolRepository

    def get_annual_summary(self, symbol: str, year: int):

        # TODO: validation layer
        # TODO: check if data exist in local db
        # TODO: if data exist in local db => return 
        # TODO: if not fetch from external API and return
        return self.symbolRepository.get_aggregated_data(symbol, year)
