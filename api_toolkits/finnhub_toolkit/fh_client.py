"""Finnhub API client implementation using official Python client."""
from typing import Dict, Any, Optional, List, Union
import finnhub
from datetime import datetime
from ..config import APIConfig

class FinnhubClient:
    """Client for interacting with the Finnhub API using official client."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the Finnhub client.
        
        Args:
            api_key: Optional API key (will use environment variable if not provided)
        """
        self.api_key = api_key or APIConfig.FINNHUB_API_KEY
        if not self.api_key:
            raise ValueError("Finnhub API key is required")
            
        self.client = finnhub.Client(api_key=self.api_key)
    
    def get_stock_candles(
        self,
        symbol: str,
        resolution: str = 'D',
        from_date: Union[int, datetime, str] = None,
        to_date: Union[int, datetime, str] = None
    ) -> Dict[str, Any]:
        """Get candlestick data for stocks.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            resolution: Supported resolution includes: 1, 5, 15, 30, 60, D, W, M
            from_date: UNIX timestamp, datetime, or YYYY-MM-DD string
            to_date: UNIX timestamp, datetime, or YYYY-MM-DD string
            
        Returns:
            Candlestick data
        """
        # Convert datetime to timestamp if needed
        if isinstance(from_date, datetime):
            from_date = int(from_date.timestamp())
        elif isinstance(from_date, str):
            from_date = int(datetime.strptime(from_date, "%Y-%m-%d").timestamp())
            
        if isinstance(to_date, datetime):
            to_date = int(to_date.timestamp())
        elif isinstance(to_date, str):
            to_date = int(datetime.strptime(to_date, "%Y-%m-%d").timestamp())
            
        return self.client.stock_candles(symbol, resolution, from_date, to_date)
    
    def get_company_profile(self, symbol: Optional[str] = None, isin: Optional[str] = None, cusip: Optional[str] = None) -> Dict[str, Any]:
        """Get general information of a company.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            isin: ISIN identifier
            cusip: CUSIP identifier
            
        Returns:
            Company profile data
        """
        return self.client.company_profile2(symbol=symbol, isin=isin, cusip=cusip)
    
    def get_quote(self, symbol: str) -> Dict[str, Any]:
        """Get real-time quote data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Real-time quote data
        """
        return self.client.quote(symbol)
    
    def get_company_news(
        self,
        symbol: str,
        from_date: Union[str, datetime],
        to_date: Union[str, datetime]
    ) -> List[Dict[str, Any]]:
        """Get company news.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            from_date: From date (YYYY-MM-DD) or datetime
            to_date: To date (YYYY-MM-DD) or datetime
            
        Returns:
            List of news items
        """
        # Convert datetime to string if needed
        if isinstance(from_date, datetime):
            from_date = from_date.strftime("%Y-%m-%d")
        if isinstance(to_date, datetime):
            to_date = to_date.strftime("%Y-%m-%d")
            
        return self.client.company_news(symbol, _from=from_date, to=to_date)
    
    def get_company_peers(self, symbol: str) -> List[str]:
        """Get company peers.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            List of peer symbols
        """
        return self.client.company_peers(symbol)
    
    def get_price_target(self, symbol: str) -> Dict[str, Any]:
        """Get latest price target consensus.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            Price target data
        """
        return self.client.price_target(symbol)
    
    def get_earnings_calendar(
        self,
        from_date: Union[str, datetime],
        to_date: Union[str, datetime],
        symbol: str = "",
        international: bool = False
    ) -> List[Dict[str, Any]]:
        """Get earnings calendar.
        
        Args:
            from_date: From date (YYYY-MM-DD) or datetime
            to_date: To date (YYYY-MM-DD) or datetime
            symbol: Symbol to filter by
            international: Include international markets
            
        Returns:
            List of earnings calendar events
        """
        if isinstance(from_date, datetime):
            from_date = from_date.strftime("%Y-%m-%d")
        if isinstance(to_date, datetime):
            to_date = to_date.strftime("%Y-%m-%d")
            
        return self.client.earnings_calendar(
            _from=from_date,
            to=to_date,
            symbol=symbol,
            international=international
        )
    
    def get_recommendation_trends(self, symbol: str) -> List[Dict[str, Any]]:
        """Get recommendation trends for a symbol.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            
        Returns:
            List of recommendation trends
        """
        return self.client.recommendation_trends(symbol)
    
    def get_stock_symbols(self, exchange: str = 'US') -> List[Dict[str, Any]]:
        """Get list of stocks.
        
        Args:
            exchange: Exchange code (e.g., 'US' for US exchanges)
            
        Returns:
            List of stocks
        """
        return self.client.stock_symbols(exchange)
    
    def get_company_earnings(self, symbol: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Get company earnings data.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            limit: Number of periods to return
            
        Returns:
            List of earnings data
        """
        return self.client.company_earnings(symbol, limit)
    
    def get_company_financials(
        self,
        symbol: str,
        statement: str = 'bs',
        freq: str = 'annual'
    ) -> Dict[str, Any]:
        """Get company financial statements.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            statement: Statement type ('bs'=Balance Sheet, 'ic'=Income Statement, 'cf'=Cash Flow)
            freq: Frequency ('annual' or 'quarterly')
            
        Returns:
            Financial statement data
        """
        return self.client.financials(symbol, statement, freq)
    
    def get_market_news(self, category: str = 'general', min_id: int = 0) -> List[Dict[str, Any]]:
        """Get market news.
        
        Args:
            category: News category ('general', 'forex', 'crypto', 'merger')
            min_id: Get news after this ID
            
        Returns:
            List of news items
        """
        return self.client.general_news(category, min_id=min_id)
    
    def get_ipo_calendar(
        self,
        from_date: Union[str, datetime],
        to_date: Union[str, datetime]
    ) -> Dict[str, Any]:
        """Get IPO calendar.
        
        Args:
            from_date: From date (YYYY-MM-DD) or datetime
            to_date: To date (YYYY-MM-DD) or datetime
            
        Returns:
            IPO calendar data
        """
        if isinstance(from_date, datetime):
            from_date = from_date.strftime("%Y-%m-%d")
        if isinstance(to_date, datetime):
            to_date = to_date.strftime("%Y-%m-%d")
            
        return self.client.ipo_calendar(_from=from_date, to=to_date)
    
    def get_earnings_estimates(
        self,
        symbol: str,
        freq: str = 'quarterly'
    ) -> Dict[str, Any]:
        """Get company's EPS estimates.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            freq: Frequency ('annual' or 'quarterly')
            
        Returns:
            EPS estimates data
        """
        return self.client.company_eps_estimates(symbol, freq)
    
    def get_stock_dividends(
        self,
        symbol: str,
        from_date: Union[str, datetime],
        to_date: Union[str, datetime]
    ) -> List[Dict[str, Any]]:
        """Get dividend history for a stock.
        
        Args:
            symbol: Stock symbol (e.g., 'AAPL')
            from_date: From date (YYYY-MM-DD) or datetime
            to_date: To date (YYYY-MM-DD) or datetime
            
        Returns:
            List of dividend events
        """
        if isinstance(from_date, datetime):
            from_date = from_date.strftime("%Y-%m-%d")
        if isinstance(to_date, datetime):
            to_date = to_date.strftime("%Y-%m-%d")
            
        return self.client.stock_dividends(symbol, _from=from_date, to=to_date)
    
    def close(self):
        """Close the client session."""
        # No explicit close needed for finnhub client
        pass 