from app.repository.SymbolRepository import SymbolRepository
from app.external.AlphaVantageAdapter import AlphaVantageAdapter
from app.service.SymbolService import SymbolService
from app.repository.DatabaseManager import DatabaseManager
from app.api.StockRouter import create_stock_router

class Factory:
    def __init__(self):
        # Create ALL dependencies here
        self.db_manager = DatabaseManager()
        self.adapter = AlphaVantageAdapter()
        self.repository = SymbolRepository(self.db_manager)
        self.symbol_service = SymbolService(self.repository, self.adapter)

        # initialize database
        self.db_manager.init_db()
    
    def get_symbol_service(self):
        return self.symbol_service
    
    def get_stock_router(self):
        # Create router with service
        return create_stock_router(self.symbol_service)