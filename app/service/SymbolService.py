from app.repository.SymbolRepository import SymbolRepository
from app.external.IStockDataProvider import IStockDataProvider
from datetime import datetime

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
        # Step 1: Get aggregated data AND last fetch date in single query
        db_data, last_fetch_date = self.symbolRepository.get_aggregated_data_with_fetch_date(symbol, year)

        if self._is_data_fresh_enough(last_fetch_date, year):
            print("Data is fresh enough. Returning from local db...")
            return db_data

        # Step 2: Data not in DB or not updated recently - fetch from external provider
        try:
            print("Data is stale or missing ==> Fetching from external service")
            monthly_data = self.stockDataProvider.fetch_monthly_data(symbol)

            # Step 3: Save fetched data to database
            self.symbolRepository.save_monthly_data(symbol, monthly_data)

            # Step 4: Aggregate and return data from the fetched monthly data
            aggregated = self.symbolRepository.get_aggregated_data(symbol, year)
            return aggregated
        except Exception as e:
            raise Exception(f"Failed to get data for {symbol}: {str(e)}")
        
    def _is_data_fresh_enough(self, last_fetch_date: datetime, inputYear: int):
        if last_fetch_date is None:
            return False
        if last_fetch_date.year > inputYear:
            # looking for a older year where we already cached the data
            return True
        # looking for the same year as last fetched year.
        # Need to get updated data if last fetch is older than 30 days
        return (datetime.now() - last_fetch_date).days < 30
    
