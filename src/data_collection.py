import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
import pickle
from typing import Dict, List, Optional
from .config import SP500_TOP_50, RAW_DATA_DIR, START_DATE, END_DATE, SECTOR_MAPPING

class FinancialDataCollector:               # collect and manage financial data
    
    def __init__(self, tickers: List[str] = None):
        self.tickers = tickers or SP500_TOP_50
        self.raw_data_path = RAW_DATA_DIR
        

    def collect_stock_data(self, period: str = "2y", save_data: bool = True) -> Dict:           # collect stock price data for specific tickers

        print(f"Collecting data for {len(self.tickers)} stocks...")
        stock_data = {}

        for i, ticker in enumerate(self.tickers):
            try:
                print(f"Processing {ticker} ({i+1}/{len(self.tickers)})")
                
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)         # get historical data

                info = stock.info                           # get company info

                hist['Returns'] = hist['Close'].pct_change()
                hist['Volatility'] = hist['Returns'].rolling(window=30).std()
                hist['MA_20'] = hist['Close'].rolling(window=20).mean()
                hist['MA_50'] = hist['Close'].rolling(window=50).mean()
                hist['RSI'] = self._calculate_rsi(hist['Close'])

                stock_data[ticker] = {
                    'prices': hist,
                    'info': info,
                    'sector': self._get_sector(ticker)
                }

            except Exception as e:
                print(f"Error collecting data for {ticker}: {e}")
                continue
        
        if save_data:
            self._save_stock_data(stock_data)
        
        return stock_data
    

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:     # Calculate RSI

        delta = prices.diff()
        gain = (delta.where(delta>0, 0)).rolling(window = period).mean()
        loss = (-delta.where(delta <0, 0)).rolling(window=period).mean()

        rs = gain/loss
        rsi = 100 - (100/(1+rs))

        return rsi


    def _get_sector(self, ticker: str) -> str:              # get sector for a given ticker

        for sector, tickers in SECTOR_MAPPING.items():
            if ticker in tickers:
                return sector
        
        return 'Other'
    
    def _save_stock_data(self, data: Dict):         # save stock data to pickle file

        filepath = os.path.join(self.raw_data_path, 'stock_data.pkl')
        with open(filepath, 'wb') as f:
            pickle.dump(data, f)
        print(f"Data saved to {filepath}")

    def load_stock_data(self) -> Dict:              # load stock data from pickle file

        filepath = os.path.join(self.raw_data_path, 'stock_data.pkl')
        try:
            with open(filepath, 'rb') as f:
                data = pickle.load(f)
            print(f"Data loaded from {filepath}")
            return data
        except FileNotFoundError:
            print("No saved data found. Collecting fresh data...")
            return self.collect_stock_data()


    def get_market_data(self) -> pd.DataFrame:          # get market indices data

        market_indices = ['^GSPC', '^DJI', '^IXIC', '^VIX']
        market_data = {}

        for index in market_indices:
            try:
                ticker = yf.Ticker(index)
                hist = ticker.history(period = "2y")
                market_data[index] = hist
            except Exception as e:
                print(f"Error collecting {index}: {e}")
        
        return market_data
    

    def create_master_dataframe(self, stock_data: Dict) -> pd.DateFrame:        # create a master dataframe with all stock prices

        price_data = {}
        
        for ticker, data in stock_data.items():
            if 'prices' in data:
                price_data[ticker] = data['prices']['Close']

        df = pd.DataFrame(price_data)
        df.index = pd.to_datetime(df.index)
        return df
        







