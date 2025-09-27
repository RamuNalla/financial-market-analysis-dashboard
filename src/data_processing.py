import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from config import PROCESSED_DATA_DIR
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
    
    def _calculate_max_drawdown(self, returns: pd.Series) -> float:     # max drawdown is the largest peak to trough decline in a portfolio during a specific period

        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max)/running_max
        return drawdown.min()
    
    def calculate_correlation_matrix(self, tickers: List[str] = None) -> pd.DataFrame:  # calculate correlation matrix for stock returns

        if tickers is None:
            tickers = list(self.stock_data.keys()) 

        returns_data = {}

        for ticker in tickers:
            if ticker in self.stock_data:
                returns_data[ticker] = self.stock_data[ticker]['prices']['Returns']

        returns_df = pd.DataFrame(returns_data)
        correlation_matrix = returns_df.corr()
        
        return correlation_matrix
    

    def calculate_sector_performance(self) -> pd.DataFrame:     # calculate sector-wise performance metrics

        from .config import SECTOR_MAPPING

        sector_performance = {}

        for sector, tickers in SECTOR_MAPPING.items():
            sector_returns = []
            for ticker in tickers:
                if ticker in self.stock_data:
                    returns = self.stock_data[ticker]['prices']['Returns'].dropna()
                    sector_returns.append(returns)
        
            if sector_returns:                          # equal weighted sector returns
                sector_df = pd.DataFrame({f"{sector}_{i}": ret for i, ret in enumerate(sector_returns)})
                avg_returns = sector_df.mean(axis=1)

                sector_performance[sector] = {
                    'annual_return': avg_returns.mean() * 252,
                    'annual_volatility': avg_returns.std() * np.sqrt(252),
                    'sharpe_ratio': (avg_returns.mean() * 252) / (avg_returns.std() * np.sqrt(252)),
                    'returns': avg_returns
                }

        return sector_performance
    

    def calculate_risk_metrics(self, ticker: str) -> Dict:          # calculate comprehensive risk metrics for a stock

        if ticker not in self.stock_data:
            return {}
        
        prices = self.stock_data[ticker]['prices']
        returns = prices['Returns'].dropna()

        var_95 = np.percentile(returns, 5)              # value at Risk (vaR) (maximum potential loss over a given timeframe)
        var_99 = np.percentile(returns, 1)

        cvar_95 = returns[returns <= var_95].mean()     # average loss that occurs when the return is worse than VaR
        cvar_99 = returns[returns <= var_99].mean()

        risk_metrics = {
            'volatility': returns.std() * np.sqrt(252),
            'var_95': var_95,
            'var_99': var_99,
            'cvar_95': cvar_95,
            'cvar_99': cvar_99,
            'skewness': returns.skew(),                 # skewness: measure of asymmetry of return distribution. 
            'kurtosis': returns.kurtosis(),             # kurtosis: measures the tailedness of a distribution
            'max_daily_loss': returns.min(),
            'max_daily_gain': returns.max()
        }

        return risk_metrics
    
    def save_processed_data(self, data: Dict, filename: str):       # save processed data to a file

        filepath = os.path.join(self.processed_data_path, filename)

        if isinstance(data, pd.DataFrame):
            data.to_csv(filepath)
        else:
            import pickle
            with open(filepath, 'wb') as f:
                pickle.dump(data, f)
        
        print(f"Processed data saved to {filepath}")

    

# 



