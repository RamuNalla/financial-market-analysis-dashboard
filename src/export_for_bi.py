import pandas as pd
import numpy as np
import sys
import os

# Add project root to Python path to allow imports from src
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.data_collection import FinancialDataCollector
from src.data_processing import FinancialDataProcessor
from src.config import SECTOR_MAPPING

def export_data_for_bi():
    """Export all necessary data for BI tools."""
    
    # Load data
    collector = FinancialDataCollector()
    stock_data = collector.load_stock_data()
    processor = FinancialDataProcessor(stock_data)
    
    # 1. Master dataset for time series analysis
    print("Creating master dataset...")
    master_data = []
    
    for ticker, data in stock_data.items():
        prices = data['prices']
        info = data['info']
        
        # Get sector
        sector = 'Other'
        for sect, tickers in SECTOR_MAPPING.items():
            if ticker in tickers:
                sector = sect
                break
        
        for date, row in prices.iterrows():
            master_data.append({
                'Date': date.strftime('%Y-%m-%d'),
                'Year': date.year,
                'Month': date.month,
                'Quarter': f"Q{((date.month-1)//3)+1} {date.year}",
                'Ticker': ticker,
                'Company_Name': info.get('longName', ticker),
                'Sector': sector,
                'Industry': info.get('industry', 'Unknown'),
                'Market_Cap_Billions': info.get('marketCap', 0) / 1e9,
                'Open': round(row['Open'], 2),
                'High': round(row['High'], 2),
                'Low': round(row['Low'], 2),
                'Close': round(row['Close'], 2),
                'Volume': int(row['Volume']),
                'Daily_Return_Pct': round(row.get('Returns', 0) * 100, 4),
                'MA_20': round(row.get('MA_20', 0), 2),
                'MA_50': round(row.get('MA_50', 0), 2),
                'RSI': round(row.get('RSI', 0), 2)
            })
    
    master_df = pd.DataFrame(master_data)
    master_df.to_csv('..notebooks/data/processed/bi_master_data.csv', index=False)
    print(f"Master dataset created: {len(master_df)} rows")
    
    # 2. Company information table
    print("Creating company info table...")
    company_info = []
    for ticker, data in stock_data.items():
        info = data['info']
        
        # Get sector
        sector = 'Other'
        for sect, tickers in SECTOR_MAPPING.items():
            if ticker in tickers:
                sector = sect
                break
        
        # Calculate key metrics
        prices = data['prices']['Close']
        returns = data['prices']['Returns'].dropna()
        
        company_info.append({
            'Ticker': ticker,
            'Company_Name': info.get('longName', ticker),
            'Sector': sector,
            'Industry': info.get('industry', 'Unknown'),
            'Market_Cap_Billions': round(info.get('marketCap', 0) / 1e9, 2),
            'Current_Price': round(prices.iloc[-1], 2),
            'Price_52W_High': round(prices.max(), 2),
            'Price_52W_Low': round(prices.min(), 2),
            'YTD_Return_Pct': round(((prices.iloc[-1] - prices.iloc[0]) / prices.iloc[0]) * 100, 2),
            'Annual_Volatility_Pct': round(returns.std() * np.sqrt(252) * 100, 2),
            'Average_Volume': int(data['prices']['Volume'].mean()),
            'Employee_Count': info.get('fullTimeEmployees', 0),
            'Country': info.get('country', 'Unknown'),
            'Website': info.get('website', ''),
            'Business_Summary': info.get('longBusinessSummary', '')[:200] + '...' if info.get('longBusinessSummary') else ''
        })
    
    company_df = pd.DataFrame(company_info)
    company_df.to_csv('../data/processed/bi_company_info.csv', index=False)
    print(f"Company info created: {len(company_df)} companies")
    
    # 3. Sector performance summary
    print("Creating sector performance table...")
    sector_performance = []
    
    for sector, tickers in SECTOR_MAPPING.items():
        sector_stocks = [t for t in tickers if t in stock_data]
        if not sector_stocks:
            continue
            
        sector_returns = []
        sector_market_cap = 0
        sector_volume = 0
        
        for ticker in sector_stocks:
            returns = stock_data[ticker]['prices']['Returns'].dropna()
            annual_return = returns.mean() * 252 * 100
            market_cap = stock_data[ticker]['info'].get('marketCap', 0) / 1e9
            avg_volume = stock_data[ticker]['prices']['Volume'].mean()
            
            sector_returns.append(annual_return)
            sector_market_cap += market_cap
            sector_volume += avg_volume
        
        sector_performance.append({
            'Sector': sector,
            'Stock_Count': len(sector_stocks),
            'Total_Market_Cap_Billions': round(sector_market_cap, 2),
            'Avg_Annual_Return_Pct': round(np.mean(sector_returns), 2),
            'Return_Volatility_Pct': round(np.std(sector_returns), 2),
            'Total_Avg_Volume': int(sector_volume),
            'Best_Performer': max(sector_stocks, key=lambda x: ((stock_data[x]['prices']['Close'].iloc[-1] - stock_data[x]['prices']['Close'].iloc[0]) / stock_data[x]['prices']['Close'].iloc[0]) * 100),
            'Worst_Performer': min(sector_stocks, key=lambda x: ((stock_data[x]['prices']['Close'].iloc[-1] - stock_data[x]['prices']['Close'].iloc[0]) / stock_data[x]['prices']['Close'].iloc[0]) * 100)
        })
    
    sector_df = pd.DataFrame(sector_performance)
    sector_df.to_csv('../data/processed/bi_sector_performance.csv', index=False)
    print(f"Sector performance created: {len(sector_df)} sectors")
    
    # 4. Monthly performance summary
    print("Creating monthly performance table...")
    monthly_data = []
    
    for ticker in list(stock_data.keys())[:20]:  # Top 20 stocks for performance
        prices = stock_data[ticker]['prices']
        monthly_prices = prices['Close'].resample('M').last()
        monthly_returns = monthly_prices.pct_change().dropna() * 100
        
        for date, return_pct in monthly_returns.items():
            monthly_data.append({
                'Year_Month': date.strftime('%Y-%m'),
                'Year': date.year,
                'Month': date.month,
                'Month_Name': date.strftime('%B'),
                'Ticker': ticker,
                'Monthly_Return_Pct': round(return_pct, 2),
                'Month_End_Price': round(monthly_prices[date], 2)
            })
    
    monthly_df = pd.DataFrame(monthly_data)
    monthly_df.to_csv('../data/processed/bi_monthly_performance.csv', index=False)
    print(f"Monthly performance created: {len(monthly_df)} records")
    
    print("\n✅ All BI data exports completed!")
    print("Files created:")
    print("- bi_master_data.csv (main dataset)")
    print("- bi_company_info.csv (company details)")
    print("- bi_sector_performance.csv (sector summaries)")
    print("- bi_monthly_performance.csv (monthly returns)")

if __name__ == "__main__":
    export_data_for_bi()