class StockAppException(Exception):
    """Base exception for our app"""
    pass

class DataNotFoundError(StockAppException):
    """Raised when the DB and API both have no data for a year"""
    pass

class ExternalAPIError(StockAppException):
    """Raised when Alpha Vantage fails"""
    pass

class ValidationError(StockAppException):
    """Raised when input validation fails"""
    pass