"""TwelveData API client implementation using official Python client."""
from typing import Dict, Any, Optional, List, Union
from twelvedata import TDClient
from ..config import APIConfig

class TwelveDataClient:
    """Client for interacting with the TwelveData API using official client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TwelveData client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        self.api_key = api_key or APIConfig.TWELVEDATA_API_KEY
        if not self.api_key:
            raise ValueError("TwelveData API key is required")
            
        self.client = TDClient(apikey=self.api_key)
    
    def get_time_series(
        self,
        symbol: str,
        interval: str = '1day',
        outputsize: int = 30,
        timezone: str = "UTC",
        **kwargs
    ) -> Dict[str, Any]:
        """Get time series data for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '1hour', '1day', '1week', '1month')
            outputsize: Number of data points (1-5000)
            timezone: Timezone for timestamps
            **kwargs: Additional parameters to pass to the time_series method
            
        Returns:
            Time series data in JSON format
        """
        ts = self.client.time_series(
            symbol=symbol,
            interval=interval,
            outputsize=outputsize,
            timezone=timezone,
            **kwargs
        )
        return ts.as_json()
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Real-time quote data
        """
        return self.client.quote(symbol=symbol).as_json()
    
    def get_price(self, symbol: str) -> Dict[str, Any]:
        """Get latest price for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Latest price data
        """
        return self.client.price(symbol=symbol).as_json()
    
    def get_stocks_list(
        self,
        exchange: Optional[str] = None,
        type: Optional[str] = None,
        symbol: Optional[str] = None,
        show_plan: bool = False
    ) -> List[Dict[str, Any]]:
        """Get list of available stocks.
        
        Args:
            exchange: Filter by exchange (e.g., 'NASDAQ')
            type: Filter by type ('Common Stock', 'ETF', etc.)
            symbol: Filter by symbol pattern
            show_plan: Show API plan details
            
        Returns:
            List of stocks matching the criteria
        """
        return self.client.stocks(
            exchange=exchange,
            type=type,
            symbol=symbol,
            show_plan=show_plan
        ).as_json()
    
    def get_technical_indicator(
        self,
        symbol: str,
        interval: str,
        indicator: str,
        series_type: str = "close",
        **kwargs
    ) -> Dict[str, Any]:
        """Get technical indicator values.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '1hour', '1day', etc.)
            indicator: Indicator name ('sma', 'ema', 'rsi', etc.)
            series_type: Type of series to use ('close', 'open', 'high', 'low')
            **kwargs: Additional parameters required by the indicator
            
        Returns:
            Technical indicator data
        """
        indicator_method = getattr(self.client, indicator.lower())
        return indicator_method(
            symbol=symbol,
            interval=interval,
            series_type=series_type,
            **kwargs
        ).as_json()
    
    def get_cryptocurrency_list(self) -> List[Dict[str, Any]]:
        """Get list of available cryptocurrencies.
        
        Returns:
            List of available cryptocurrencies
        """
        return self.client.cryptocurrencies().as_json()
    
    def get_forex_pairs(self) -> List[Dict[str, Any]]:
        """Get list of available forex pairs.
        
        Returns:
            List of available forex pairs
        """
        return self.client.forex_pairs().as_json()
    
    def get_earliest_timestamp(
        self,
        symbol: str,
        interval: str,
        exchange: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get the earliest available timestamp for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            interval: Time interval ('1min', '5min', '1hour', '1day', etc.)
            exchange: Specific exchange (optional)
            
        Returns:
            Earliest timestamp information
        """
        return self.client.earliest_timestamp(
            symbol=symbol,
            interval=interval,
            exchange=exchange
        ).as_json() 