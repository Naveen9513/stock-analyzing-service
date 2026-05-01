
from fastapi import APIRouter, Depends
from app.service.SymbolService import SymbolService

# Using a prefix keeps your URLs clean
router = APIRouter(prefix="/symbols")

# Creates the service and its requirements
def get_symbol_service():
    # In the future, you'll pass your actual Repo and API Client here
    return SymbolService()

@router.get("/{symbol}/annual/{year}")
def get_annual_data(
    symbol: str, 
    year: int, 
    service: SymbolService = Depends(get_symbol_service)):
    """
    Fetches stock annual stats for a given symbol
    """
    
    # Logic for Requirement #7-11 will go here:
    # 1. db_data = repository.get_data(symbol, year)
    # 2. if not db_data: fetch from alpha vantage...
    
    return service.get_annual_summary(symbol, year)