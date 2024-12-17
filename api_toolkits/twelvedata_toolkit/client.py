"""TwelveData API client implementation."""
from typing import Dict, Any, Optional, List, Union
from ..base_client import BaseAPIClient
from ..config import APIConfig

class TwelveDataClient(BaseAPIClient):
    """Client for interacting with the TwelveData API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TwelveData client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        api_key = api_key or APIConfig.TWELVEDATA_API_KEY
        if not api_key:
            raise ValueError("TwelveData API key is required")
            
        super().__init__(
            api_key=api_key,
            base_url=APIConfig.TWELVEDATA_BASE_URL,
            calls_per_minute=APIConfig.TWELVEDATA_RATE_LIMIT
        )
    
    def get_time_series(
        self,
        symbol: str,
        interval: str = '1day',
        outputsize: int = 30,
        format: str = 'JSON'
    ) -> Dict[str, Any]:
        """Get time series data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '1hour', '1day', '1week', '1month')
            outputsize: Number of data points (1-5000)
            format: Output format ('JSON' or 'CSV')
            
        Returns:
            Time series data
        """
        return self._make_request(
            endpoint='time_series',
            params={
                'symbol': symbol,
                'interval': interval,
                'outputsize': outputsize,
                'format': format,
                'apikey': self.api_key
            }
        )
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Real-time quote data
        """
        return self._make_request(
            endpoint='quote',
            params={
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get latest price for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Latest price data
        """
        return self._make_request(
            endpoint='price',
            params={
                'symbol': symbol,
                'apikey': self.api_key
            }
        )
    
    def get_stocks_list(
        self,
        exchange: Optional[str] = None,
        country: Optional[str] = None,
        type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get list of available stocks.
        
        Args:
            exchange: Filter by exchange (e.g., 'NASDAQ')
            country: Filter by country (e.g., 'United States')
            type: Filter by type ('Common Stock', 'ETF', etc.)
            
        Returns:
            List of stocks matching the criteria
        """
        params = {'apikey': self.api_key}
        if exchange:
            params['exchange'] = exchange
        if country:
            params['country'] = country
        if type:
            params['type'] = type
            
        return self._make_request(
            endpoint='stocks',
            params=params
        )
    
    def get_technical_indicator(
        self,
        symbol: str,
        interval: str,
        indicator: str,
        indicator_fields: Optional[Dict[str, Union[int, float, str]]] = None
    ) -> Dict[str, Any]:
        """Get technical indicator values.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '1hour', '1day', etc.)
            indicator: Indicator name ('sma', 'ema', 'rsi', etc.)
            indicator_fields: Additional fields required by the indicator
            
        Returns:
            Technical indicator data
        """
        params = {
            'symbol': symbol,
            'interval': interval,
            'apikey': self.api_key
        }
        
        if indicator_fields:
            params.update(indicator_fields)
            
        return self._make_request(
            endpoint=indicator,
            params=params
        ) 