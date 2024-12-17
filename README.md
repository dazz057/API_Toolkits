# Financial API Toolkits

A collection of Python toolkits for interacting with financial APIs including Finnhub, AlphaVantage, and TwelveData.

## Features

- Modular design for easy integration
- Rate limiting and error handling
- Comprehensive typing support
- Configurable through environment variables
- Consistent API across different providers

## Installation

1. Clone the repository:
```bash
git clone [your-repo-url]
cd api-toolkits
```

2. Create and activate a virtual environment:
```bash
python -m venv apivenv
source apivenv/bin/activate  # On Windows: apivenv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root with your API keys:

```env
FINNHUB_API_KEY=your_finnhub_key
ALPHAVANTAGE_API_KEY=your_alphavantage_key
TWELVEDATA_API_KEY=your_twelvedata_key
```

## Usage

### Finnhub API Example

```python
from api_toolkits.finnhub_toolkit.client import FinnhubClient

# Initialize client
client = FinnhubClient()  # Will use API key from environment variables

# Get company profile
profile = client.get_company_profile('AAPL')

# Get real-time quote
quote = client.get_quote('AAPL')

# Get news
news = client.get_news(category='general')

# Don't forget to close the client when done
client.close()
```

Similar patterns apply for AlphaVantage and TwelveData clients.

## Project Structure

```
api_toolkits/
├── __init__.py
├── config.py
├── base_client.py
├── finnhub_toolkit/
│   ├── __init__.py
│   └── client.py
├── alphavantage_toolkit/
│   ├── __init__.py
│   └── client.py
└── twelvedata_toolkit/
    ├── __init__.py
    └── client.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 