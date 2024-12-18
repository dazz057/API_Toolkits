"""Test script for TwelveData WebSocket functionality."""
import asyncio
from api_toolkits.twelvedata_toolkit import TwelveDataClient
import json
from datetime import datetime

async def on_message(message: dict) -> None:
    """Handle incoming WebSocket messages.
    
    Args:
        message: Message data from WebSocket
    """
    # Format timestamp
    timestamp = datetime.fromtimestamp(message.get('timestamp', 0))
    formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    
    print(f"\nReceived price update at {formatted_time}:")
    print(json.dumps(message, indent=2))

async def on_error(error: Exception) -> None:
    """Handle WebSocket errors.
    
    Args:
        error: Exception that occurred
    """
    print(f"Error occurred: {str(error)}")

async def test_websocket():
    """Test TwelveData WebSocket functionality."""
    client = TwelveDataClient()
    
    print("TwelveData WebSocket Test")
    print("=" * 50)
    
    while True:
        print("\nWebSocket Test Menu:")
        print("1. Subscribe to symbols")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ")
        
        if choice == "2":
            print("Exiting...")
            break
            
        if choice == "1":
            # Get symbols input
            symbols_input = input("Enter symbols (comma-separated, e.g., AAPL,MSFT,GOOGL): ")
            symbols = [s.strip() for s in symbols_input.split(",")]
            
            print(f"\nConnecting to WebSocket and subscribing to: {', '.join(symbols)}")
            print("Press Ctrl+C to stop receiving updates\n")
            
            try:
                await client.start_websocket(
                    symbols=symbols,
                    on_message=on_message,
                    on_error=on_error
                )
            except KeyboardInterrupt:
                print("\nStopping WebSocket connection...")
            finally:
                await client.close_websocket()
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    # Run the async test
    asyncio.run(test_websocket()) 