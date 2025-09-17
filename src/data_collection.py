import yfinance as yf
import pandas as pd
from datatime import datetime, timedelta

def collect_stock_data():

    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B', 'UNH', 'JNJ']

    stock_data = {}

    for ticker in tickers:
        stock = yf.Ticker(ticker)

        hist = stock.history(period="2y")       # get 2 years of historical data
        info = stock.info
        stock_data[ticker] = {
            'prices': hist,
            'info': info
        }
    return stock_data