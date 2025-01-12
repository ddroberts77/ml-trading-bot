import yfinance as yf
import pandas as pd
import os
from typing import List

class DataCollector:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)

    def download_historical_data(self, 
                                 symbols: List[str], 
                                 start_date: str = '2018-01-01', 
                                 end_date: str = '2024-01-01', 
                                 interval: str = '1d'):
        """
        Download historical financial data for multiple symbols
        
        Args:
            symbols: List of ticker symbols
            start_date: Start date for data collection
            end_date: End date for data collection
            interval: Data interval (1d, 1h, 5m, etc.)
        """
        for symbol in symbols:
            try:
                print(f"Downloading data for {symbol}")
                data = yf.download(symbol, 
                                   start=start_date, 
                                   end=end_date, 
                                   interval=interval)
                
                # Save to CSV
                filename = os.path.join(self.data_dir, f'{symbol}_historical.csv')
                data.to_csv(filename)
                print(f"Data saved to {filename}")
            
            except Exception as e:
                print(f"Error downloading {symbol}: {e}")

def main():
    # Comprehensive list of assets
    assets = [
        'BTC-USD',   # Cryptocurrency
        'AAPL',      # Technology
        'TSLA',      # Electric Vehicles
        'GOOGL',     # Internet
        'AMZN',      # E-commerce
        '^GSPC',     # S&P 500
        '^IXIC',     # NASDAQ
        'GC=F',      # Gold Futures
        'CL=F',      # Crude Oil Futures
        'EURUSD=X'   # Currency
    ]

    collector = DataCollector()
    collector.download_historical_data(assets)

if __name__ == '__main__':
    main()
