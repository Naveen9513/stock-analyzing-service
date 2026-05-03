from app.repository.SymbolRepository import SymbolRepository
from app.external.IStockDataProvider import IStockDataProvider

class SymbolService:
    def __init__(self, 
                 symbolRepository: SymbolRepository, 
                 stockDataProvider: IStockDataProvider):
        self.symbolRepository = symbolRepository
        self.stockDataProvider = stockDataProvider

    def get_annual_summary(self, symbol: str, year: int):
        """
        Get annual summary for a symbol - checks DB first, fetches from API if needed
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            year: Year to retrieve data for
        
        Returns:
            dict: Aggregated yearly data with high, low, volume
        """
        # Step 1: Check if data exists in local database
        db_data = self.symbolRepository.get_aggregated_data(symbol, year)
        
        if db_data:
            print("found in local db ==> Returning data from local db")
            return db_data
        
        # Step 2: Data not in DB - fetch from external provider
        try:
            print("can not find in local db ==> Fetching from external service")
            monthly_data = self.stockDataProvider.fetch_monthly_data(symbol)
            
            # Step 3: Save fetched data to database
            self.symbolRepository.save_monthly_data(symbol, monthly_data)
            
            # Step 4: Aggregate and return data from the fetched monthly data
            aggregated = self._aggregate_monthly_data(symbol, year, monthly_data["data"])
            return aggregated
        except Exception as e:
            raise Exception(f"Failed to get data for {symbol}: {str(e)}")
    
    def _aggregate_monthly_data(self, symbol: str, year: int, monthly_data: dict):
        """
        Private helper to calculate stats for a specific year from raw data.
        """
        year_str = str(year)
        highs = []
        lows = []
        total_volume = 0
        found_data = False

        for date_str, metrics in monthly_data.items():
            # Check if the date (e.g., '2026-04') belongs to the requested year
            if date_str.startswith(year_str):
                highs.append(metrics['high'])
                lows.append(metrics['low'])
                total_volume += metrics['volume']
                found_data = True

        if not found_data:
            print(f"No data found for {symbol} in {year}")
            return {
                "symbol": symbol.upper(),
                "year": year,
                "high": None,
                "low": None,
                "volume": 0,
                "note": "No data found for this specific year"
            }

        return {
            "symbol": symbol.upper(),
            "year": year,
            "high": max(highs),
            "low": min(lows),
            "volume": total_volume
        }

    
