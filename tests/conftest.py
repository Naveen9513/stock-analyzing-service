import pytest


@pytest.fixture
def mock_alpha_vantage_response():
    """Mock response from Alpha Vantage API"""
    return {
        "Monthly Time Series": {
            "2025-12-31": {
                "1. open": "250.0000",
                "2. high": "260.5000",
                "3. low": "245.0000",
                "4. close": "255.5000",
                "5. volume": "150000000"
            },
            "2025-11-28": {
                "1. open": "240.0000",
                "2. high": "250.0000",
                "3. low": "235.0000",
                "4. close": "248.0000",
                "5. volume": "140000000"
            },
            "2025-10-31": {
                "1. open": "230.0000",
                "2. high": "240.0000",
                "3. low": "225.0000",
                "4. close": "238.0000",
                "5. volume": "130000000"
            }
        }
    }


@pytest.fixture
def mock_api_error_response():
    """Mock error response from Alpha Vantage API"""
    return {
        "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute."
    }
