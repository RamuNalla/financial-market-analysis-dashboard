import yfinance as yf
import pandas as pd
from datatime import datetime, timedelta
import os
import pickle
from typing import Dict, List, Optional
from .config import SP500_TOP_50, RAW_DATA_DIR, START_DATE, END_DATE, SECTOR_MAPPING

class FinancialDataCollector:               # collect and manage financial data
    
    def __init__(self, tickers: List[str] = None):
        self.tickers = tickers or SP500_TOP_50
        self.raw_data_dir = RAW_DATA_DIR
        

    def collect_stock_data(self, period: str = "2y", save_data: bool = True) -> Dict:           # collect stock price data for specific tickers

        print(f"Collecting data for {len(self.tickers)} stocks...")
        stock_data = {}

        for i, ticker in enumerate(self.tickers):
            try:
                print(f"Processing {ticker} ({i+1}/{len(self.tickers)})")
                
                stock = yf.Ticker(ticker)
                hist = stock.history(period=period)

                info = stock.info

                hist['Returns'] = hist['Close'].pct_change()
                