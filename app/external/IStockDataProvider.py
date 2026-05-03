from abc import ABC, abstractmethod


class IStockDataProvider(ABC):
    """Abstract interface for stock data providers"""
    
    @abstractmethod
    def fetch_monthly_data(self, symbol: str) -> dict:
        """
        Fetch monthly stock data for a symbol
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
        
        Returns:
            dict: Monthly data in format {
                'symbol': 'AAPL',
                'data': {
                    '2025-01': {'open': 150.0, 'high': 160.0, 'low': 145.0, 'close': 155.0, 'volume': 1000000},
                    '2025-02': {...},
                    ...
                }
            }
        """
        pass
