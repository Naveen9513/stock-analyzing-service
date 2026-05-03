from app.repository.SymbolRepository import SymbolRepository
from app.external.IStockDataProvider import IStockDataProvider

class SymbolService:
    def __init__(self, symbolRepository: SymbolRepository, stockDataProvider: IStockDataProvider):
        self.symbolRepository = symbolRepository
        self.stockDataProvider = stockDataProvider

    def get_annual_summary(self, symbol: str, year: int):

        # TODO: validation layer
        # TODO: check if data exist in local db
        # TODO: if data exist in local db => return 
        # TODO: if not fetch from external API and return
        return self.symbolRepository.get_aggregated_data(symbol, year)
