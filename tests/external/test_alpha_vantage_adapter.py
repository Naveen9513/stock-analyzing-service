import pytest
from unittest.mock import patch, MagicMock
from app.external.AlphaVantageAdapter import AlphaVantageAdapter


class TestAlphaVantageAdapter:
    """Tests for AlphaVantageAdapter"""
    
    def test_init_with_provided_api_key(self):
        """Test adapter initialization with provided API key"""
        adapter = AlphaVantageAdapter(api_key="test_key_123")
        assert adapter.api_key == "test_key_123"
        assert adapter.base_url == "https://www.alphavantage.co/query"
    
    @patch.dict('os.environ', {'ALPHA_VANTAGE_API_KEY': 'env_key_456'})
    def test_init_with_env_api_key(self):
        """Test adapter initialization with API key from environment"""
        adapter = AlphaVantageAdapter()
        assert adapter.api_key == "env_key_456"
    
    @patch('app.external.AlphaVantageAdapter.requests.get')
    def test_fetch_monthly_data_success(self, mock_get, mock_alpha_vantage_response):
        """Test successful monthly data fetch"""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_alpha_vantage_response
        mock_get.return_value = mock_response
        
        adapter = AlphaVantageAdapter(api_key="test_key")
        result = adapter.fetch_monthly_data("AAPL")
        
        assert result['symbol'] == "AAPL"
        assert '2025-12' in result['data']
        assert result['data']['2025-12']['high'] == 260.5
        assert result['data']['2025-12']['low'] == 245.0
        assert result['data']['2025-12']['volume'] == 150000000
    
    @patch('app.external.AlphaVantageAdapter.requests.get')
    def test_fetch_monthly_data_api_error(self, mock_get, mock_api_error_response):
        """Test handling of API error response"""
        mock_response = MagicMock()
        mock_response.json.return_value = mock_api_error_response
        mock_get.return_value = mock_response
        
        adapter = AlphaVantageAdapter(api_key="test_key")
        
        with pytest.raises(Exception) as exc_info:
            adapter.fetch_monthly_data("AAPL")
        
        assert "Invalid response from Alpha Vantage" in str(exc_info.value)
    
    @patch('app.external.AlphaVantageAdapter.requests.get')
    def test_fetch_monthly_data_network_error(self, mock_get):
        """Test handling of network errors"""
        mock_get.side_effect = Exception("Network timeout")
        
        adapter = AlphaVantageAdapter(api_key="test_key")
        
        with pytest.raises(Exception) as exc_info:
            adapter.fetch_monthly_data("AAPL")
        
        assert "Error fetching data from Alpha Vantage" in str(exc_info.value)
    
    def test_parse_response_format(self, mock_alpha_vantage_response):
        """Test response parsing and data format conversion"""
        adapter = AlphaVantageAdapter(api_key="test_key")
        result = adapter._parse_response("AAPL", mock_alpha_vantage_response)
        
        assert result['symbol'] == "AAPL"
        assert isinstance(result['data'], dict)
        
        # Check data is keyed by YYYY-MM format
        for key in result['data'].keys():
            assert len(key) == 7  # YYYY-MM format
            assert key[4] == '-'
        
        # Check price data structure
        for year_month, prices in result['data'].items():
            assert 'open' in prices
            assert 'high' in prices
            assert 'low' in prices
            assert 'close' in prices
            assert 'volume' in prices
            assert isinstance(prices['open'], float)
            assert isinstance(prices['volume'], int)
