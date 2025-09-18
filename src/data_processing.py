import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from .config import PROCESSED_DATA_DIR
import os

class FinancialDataProcessor:           # process and analyze financial data

    def __init__(self, stock_data: Dict):
        self.stock_data = stock_data
        self.processed_data_path = PROCESSED_DATA_DIR
    
    def calculate_portfolio_metrics(self, tickers: List[str], weights: List[float] = None) -> Dict:     # calculate portfolio performance metrics

        if weights is None:
            weights = [1/len(tickers)] * len(tickers)

        returns_data = {}
        for ticker in tickers:
            if ticker in self.stock_data:
                returns_data[ticker] = self.stock_data[ticker]['prices']['Returns'].dropna()
        
        returns_df = pd.DataFrame 

        portfolio_returns = (returns_df * weights).sum(axis=1)      # portfolio returns

        metrics = {                                                 # calculate metrics
            'annual_return': portfolio_returns.mean() * 252,
            'annual_volatility': portfolio_returns.std() * np.sqrt(252),
            'sharpe_ratio': (portfolio_returns.mean() * 252) / (portfolio_returns.std() * np.sqrt(252)),
            'max_drawdown': self._calculate_max_drawdown(portfolio_returns),
            'total_return': (1 + portfolio_returns).cumprod().iloc[-1] - 1,
            'returns': portfolio_returns
        }
        
        return metrics
    




