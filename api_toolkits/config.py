"""Configuration management for API toolkits."""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class APIConfig:
    """Base configuration class for API settings."""
    
    FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
    ALPHAVANTAGE_API_KEY = os.getenv('ALPHAVANTAGE_API_KEY')
    TWELVEDATA_API_KEY = os.getenv('TWELVEDATA_API_KEY')
    
    # Base URLs
    FINNHUB_BASE_URL = 'https://finnhub.io/api/v1'
    ALPHAVANTAGE_BASE_URL = 'https://www.alphavantage.co/query'
    TWELVEDATA_BASE_URL = 'https://api.twelvedata.com'
    
    # Rate limits (requests per minute)
    FINNHUB_RATE_LIMIT = 60
    ALPHAVANTAGE_RATE_LIMIT = 5
    TWELVEDATA_RATE_LIMIT = 8
    
    @classmethod
    def validate_api_keys(cls):
        """Validate that all required API keys are present."""
        missing_keys = []
        if not cls.FINNHUB_API_KEY:
            missing_keys.append('FINNHUB_API_KEY')
        if not cls.ALPHAVANTAGE_API_KEY:
            missing_keys.append('ALPHAVANTAGE_API_KEY')
        if not cls.TWELVEDATA_API_KEY:
            missing_keys.append('TWELVEDATA_API_KEY')
        
        if missing_keys:
            raise ValueError(f"Missing API keys: {', '.join(missing_keys)}") 