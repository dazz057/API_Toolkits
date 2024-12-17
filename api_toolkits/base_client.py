"""Base client class for API interactions."""
import logging
from typing import Dict, Any, Optional
import requests
from ratelimit import limits, sleep_and_retry
from .config import APIConfig

class BaseAPIClient:
    """Base class for API clients with common functionality."""
    
    def __init__(self, api_key: str, base_url: str, calls_per_minute: int):
        """Initialize the base client.
        
        Args:
            api_key: API key for authentication
            base_url: Base URL for the API
            calls_per_minute: Maximum number of API calls allowed per minute
        """
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.calls_per_minute = calls_per_minute
        
        # Set up logging
        self.logger = logging.getLogger(self.__class__.__name__)
    
    @sleep_and_retry
    @limits(calls=1, period=1)  # Basic rate limiting
    def _make_request(
        self, 
        endpoint: str, 
        method: str = 'GET', 
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Make an API request with rate limiting and error handling.
        
        Args:
            endpoint: API endpoint to call
            method: HTTP method to use
            params: Query parameters for the request
            headers: Additional headers for the request
            
        Returns:
            API response as a dictionary
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                headers=headers
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            raise
    
    def _validate_response(self, response: Dict[str, Any]) -> bool:
        """Validate the API response.
        
        Args:
            response: API response to validate
            
        Returns:
            True if valid, False otherwise
        """
        return bool(response)  # Basic validation, override in subclasses
    
    def close(self):
        """Close the session."""
        self.session.close() 