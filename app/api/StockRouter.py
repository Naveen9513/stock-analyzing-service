
from fastapi import APIRouter, Depends
from app.service.SymbolService import SymbolService
from app.validator.SymbolStatRequestValidator import SymbolStatRequestValidator

def create_stock_router(symbol_service: SymbolService):
    router = APIRouter(prefix="/symbols")
    
    @router.get("/{symbol}/annual/{year}")
    def get_annual_data(params: SymbolStatRequestValidator = Depends()):
        return symbol_service.get_annual_summary(params.symbol, params.year)
    
    return router
    