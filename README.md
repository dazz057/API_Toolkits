# Financial API Toolkits

A collection of Python toolkits for interacting with financial APIs including Finnhub, AlphaVantage, and TwelveData.

## Features

- Modular design for easy integration
- Rate limiting and error handling
- Comprehensive typing support
- Configurable through environment variables
- Consistent API across different providers
- Individual and combined testing capabilities

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

## Test Scripts

The project includes several test scripts to demonstrate the functionality of each API toolkit:

### 1. Individual API Tests

- `test_finnhub.py`: Test Finnhub API functionality
  - Fetch recent news articles
  - Date range filtering
  - News article formatting

- `test_twelvedata.py`: Test TwelveData API functionality
  - Time series data
  - Technical indicators
  - Real-time quotes
  - Stock listings

- `test_alphavantage.py`: Test AlphaVantage API functionality
  - Daily time series
  - Company overviews
  - Earnings data
  - Global quotes
  - Symbol search

### 2. Combined API Test

`test_combined_apis.py` demonstrates how to use all three APIs together for comprehensive market analysis:

1. **Comprehensive Stock Analysis**
   - Company profiles
   - Technical indicators
   - Fundamental data

2. **Multi-Source Price Comparison**
   - Real-time quotes from all sources
   - Cross-validation of pricing data

3. **News and Technical Analysis**
   - Recent news articles
   - Technical indicators (RSI, MACD, SMA)
   - Market sentiment analysis

4. **Company Research**
   - Company overview
   - Earnings history
   - Analyst recommendations
   - Price action

## Usage Examples

### Individual API Usage

```python
# Finnhub Example
from api_toolkits.finnhub_toolkit import FinnhubClient

client = FinnhubClient()
news = client.get_company_news('AAPL', '2024-01-01', '2024-01-31')
client.close()

# TwelveData Example
from api_toolkits.twelvedata_toolkit import TwelveDataClient

client = TwelveDataClient()
time_series = client.get_time_series('AAPL', interval='1day', outputsize=30)

# AlphaVantage Example
from api_toolkits.alphavantage_toolkit import AlphaVantageClient

client = AlphaVantageClient()
overview = client.get_company_overview('AAPL')
client.close()
```

### Running Test Scripts

```bash
# Activate virtual environment
source apivenv/bin/activate

# Run individual tests
python test_finnhub.py
python test_twelvedata.py
python test_alphavantage.py

# Run combined test
python test_combined_apis.py
```

## Project Structure

```
api_toolkits/
├── __init__.py
├── config.py
├── base_client.py
├── finnhub_toolkit/
│   ├── __init__.py
│   └── fh_client.py
├── alphavantage_toolkit/
│   ├── __init__.py
│   └── av_client.py
└── twelvedata_toolkit/
    ├── __init__.py
    └── td_client.py
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 