import pandas as pd
import numpy as np
import ta
import os

class FeatureEngineer:
    def __init__(self, data_dir='./data'):
        self.data_dir = data_dir

    def load_data(self, filename):
        """Load historical data"""
        return pd.read_csv(os.path.join(self.data_dir, filename))

    def compute_technical_indicators(self, df):
        """
        Compute a comprehensive set of technical indicators
        
        Advanced technical indicators inspired by zero-lag and adaptive techniques
        """
        # Trend Indicators
        df['SMA_50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
        df['EMA_20'] = ta.trend.EMAIndicator(df['Close'], window=20).ema_indicator()
        
        # Momentum Indicators
        df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
        df['MACD'] = ta.trend.MACD(df['Close']).macd()
        
        # Volatility Indicators
        df['BB_High'] = ta.volatility.BollingerBands(df['Close']).bollinger_hband()
        df['BB_Low'] = ta.volatility.BollingerBands(df['Close']).bollinger_lband()
        
        return df

    def create_market_regime_features(self, df):
        """
        Classify market regimes based on technical indicators
        """
        # Identify market trends
        df['Market_Trend'] = np.where(df['Close'] > df['SMA_50'], 1, -1)
        
        # Volatility classification
        df['Volatility_Regime'] = pd.cut(
            df['BB_High'] - df['BB_Low'], 
            bins=3, 
            labels=['Low', 'Medium', 'High']
        )
        
        return df

def main():
    engineer = FeatureEngineer()
    
    # Process all data files
    for filename in os.listdir(engineer.data_dir):
        if filename.endswith('_historical.csv'):
            df = engineer.load_data(filename)
            df = engineer.compute_technical_indicators(df)
            df = engineer.create_market_regime_features(df)
            
            # Save processed data
            output_filename = f'processed_{filename}'
            df.to_csv(os.path.join(engineer.data_dir, output_filename), index=False)
            print(f"Processed {filename}")

if __name__ == '__main__':
    main()
