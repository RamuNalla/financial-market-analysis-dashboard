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