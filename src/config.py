import os
from typing import List, Dict

SP500_TOP_50 = [                                                         # Stock symbols for analysis
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B', 
    'UNH', 'JNJ', 'V', 'WMT', 'XOM', 'LLY', 'JPM', 'PG', 'MA', 'HD',
    'CVX', 'MRK', 'ABBV', 'PEP', 'KO', 'AVGO', 'PFE', 'TMO', 'COST',
    'BAC', 'NFLX', 'CRM', 'ACN', 'LIN', 'MCD', 'ABT', 'ADBE', 'DHR',
    'VZ', 'WFC', 'NEE', 'CMCSA', 'PM', 'NKE', 'TXN', 'RTX', 'UNP',
    'LOW', 'AMD', 'T', 'QCOM', 'HON'
]

SECTOR_MAPPING = {                                                                          # Mapping of sectors to their respective stock symbols                                                          
    'Technology': ['AAPL', 'MSFT', 'GOOGL', 'META', 'NVDA', 'CRM', 'ADBE', 'AMD', 'TXN', 'QCOM'],
    'Healthcare': ['UNH', 'JNJ', 'LLY', 'PFE', 'TMO', 'MRK', 'ABBV', 'ABT', 'DHR'],
    'Financial': ['BRK-B', 'V', 'JPM', 'MA', 'BAC', 'WFC'],
    'Consumer': ['AMZN', 'TSLA', 'WMT', 'PG', 'HD', 'COST', 'MCD', 'NKE', 'LOW'],
    'Energy': ['XOM', 'CVX'],
    'Communication': ['NFLX', 'VZ', 'CMCSA', 'T'],
    'Industrial': ['RTX', 'UNP', 'HON'],
    'Materials': ['LIN'],
    'Utilities': ['NEE'],
    'Consumer Staples': ['PEP', 'KO', 'PM']
}

DATA_DIR = 'data'
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, 'processed')    
EXTERNAL_DATA_DIR = os.path.join(DATA_DIR, 'external')

for directory in [DATA_DIR, RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR]:
    os.makedirs(directory, exist_ok=True)

PLOT_STYLE = 'seaborn-v0_8'
COLOR_PALETTE = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                 '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']

START_DATE = '2022-01-01'
END_DATE = '2024-12-31'