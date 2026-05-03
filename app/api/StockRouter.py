
from fastapi import APIRouter, Depends
from app.service.SymbolService import SymbolService

def create_stock_router(symbol_service: SymbolService):
    router = APIRouter(prefix="/symbols")
    
    @router.get("/{symbol}/annual/{year}")
    def get_annual_data(symbol: str, year: int):
        return symbol_service.get_annual_summary(symbol, year)
    
    return router
    