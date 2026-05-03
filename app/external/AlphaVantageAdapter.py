import os
import requests
from app.external.IStockDataProvider import IStockDataProvider


class AlphaVantageAdapter(IStockDataProvider):
    """Adapter for Alpha Vantage API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        self.base_url = os.getenv('ALPHA_VANTAGE_URL', 'https://www.alphavantage.co/query')
    
    def fetch_monthly_data(self, symbol: str) -> dict:
        """
        Fetch monthly stock data from Alpha Vantage
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
        
        Returns:
            dict: Monthly data parsed from Alpha Vantage response
        """
        params = {
            'function': 'TIME_SERIES_MONTHLY',
            'symbol': symbol,
            'apikey': self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            # Parse the response
            return self._parse_response(symbol, data)
        except Exception as e:
            raise Exception(f"Error fetching data from Alpha Vantage: {str(e)}")
    
    def _parse_response(self, symbol: str, api_response: dict) -> dict:
        """
        Parse Alpha Vantage API response into our format
        
        Args:
            symbol: Stock symbol
            api_response: Raw response from Alpha Vantage
        
        Returns:
            dict: Parsed monthly data
        """
        time_series_key = 'Monthly Time Series'
        
        if time_series_key not in api_response:
            raise Exception(f"Invalid response from Alpha Vantage: {api_response.get('Note', 'Unknown error')}")
        
        monthly_data = {}
        for date_str, day_data in api_response[time_series_key].items():
            # Convert date format YYYY-MM-DD to YYYY-MM
            year_month = date_str[:7]
            
            monthly_data[year_month] = {
                'open': float(day_data.get('1. open', 0)),
                'high': float(day_data.get('2. high', 0)),
                'low': float(day_data.get('3. low', 0)),
                'close': float(day_data.get('4. close', 0)),
                'volume': int(day_data.get('5. volume', 0))
            }
        
        return {
            'symbol': symbol,
            'data': monthly_data
        }
