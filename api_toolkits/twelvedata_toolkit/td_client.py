"""TwelveData API client implementation using official Python client."""
from typing import Dict, Any, Optional, List, Union, Callable
from twelvedata import TDClient
import websockets
import asyncio
import json
from ..config import APIConfig

class TwelveDataClient:
    """Client for interacting with the TwelveData API using official client."""
    
    WEBSOCKET_URL = "wss://ws.twelvedata.com/v1/quotes/price"
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the TwelveData client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        self.api_key = api_key or APIConfig.TWELVEDATA_API_KEY
        if not self.api_key:
            raise ValueError("TwelveData API key is required")
            
        self.client = TDClient(apikey=self.api_key)
        self.ws = None
        self._running = False
    
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
    
    async def connect_websocket(self) -> None:
        """Connect to TwelveData WebSocket server."""
        if self.ws is not None:
            return
            
        url = f"{self.WEBSOCKET_URL}?apikey={self.api_key}"
        self.ws = await websockets.connect(url)
        self._running = True
    
    async def subscribe(self, symbols: Union[str, List[str]]) -> None:
        """Subscribe to real-time price updates for symbols.
        
        Args:
            symbols: Single symbol or list of symbols to subscribe to
        """
        if isinstance(symbols, str):
            symbols = [symbols]
            
        if not self.ws:
            await self.connect_websocket()
            
        message = {
            "action": "subscribe",
            "params": {
                "symbols": ",".join(symbols)
            }
        }
        
        await self.ws.send(json.dumps(message))
    
    async def unsubscribe(self, symbols: Union[str, List[str]]) -> None:
        """Unsubscribe from real-time price updates for symbols.
        
        Args:
            symbols: Single symbol or list of symbols to unsubscribe from
        """
        if isinstance(symbols, str):
            symbols = [symbols]
            
        if not self.ws:
            return
            
        message = {
            "action": "unsubscribe",
            "params": {
                "symbols": ",".join(symbols)
            }
        }
        
        await self.ws.send(json.dumps(message))
    
    async def start_websocket(
        self,
        symbols: Union[str, List[str]],
        on_message: Callable[[Dict[str, Any]], None],
        on_error: Optional[Callable[[Exception], None]] = None
    ) -> None:
        """Start WebSocket connection and handle incoming messages.
        
        Args:
            symbols: Symbols to subscribe to
            on_message: Callback function for handling incoming messages
            on_error: Optional callback function for handling errors
        """
        try:
            await self.connect_websocket()
            await self.subscribe(symbols)
            
            while self._running:
                try:
                    message = await self.ws.recv()
                    data = json.loads(message)
                    await on_message(data)
                except Exception as e:
                    if on_error:
                        await on_error(e)
                    else:
                        print(f"WebSocket error: {str(e)}")
                        
        finally:
            await self.close_websocket()
    
    async def close_websocket(self) -> None:
        """Close the WebSocket connection."""
        self._running = False
        if self.ws:
            await self.ws.close()
            self.ws = None
    
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