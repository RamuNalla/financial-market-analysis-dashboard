import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Dict, Tuple
from config import COLOR_PALETTE, PLOT_STYLE

class VisualizationUtils:           # utility functions for creating visulaizations

    def __init__(self):
        plt.style.use(PLOT_STYLE)
        sns.set_palette(COLOR_PALETTE)

    @staticmethod
    def setup_plot_style():                 # setup consistent plot styling
        plt.rcParams.update({
            'figure.figsize': (12, 8),
            'font.size': 10,
            'axes.labelsize': 12,
            'axes.titlesize': 14,
            'xtick.labelsize': 10,
            'ytick.labelsize': 10,
            'legend.fontsize': 10,
            'figure.titlesize': 16
        })

    @staticmethod
    def create_subplot_grid(nrows: int, ncols: int, figsize: Tuple[int, int] = (15, 10)):       # create a subplot grid with consistent styling
        fig, axes = plt.subplots(nrows, ncols, figsize=figsize)
        fig.suptitle('Financial Market Analysis', fontsize=16, y=0.98)
        plt.tight_layout()
        return fig, axes
    
    @staticmethod
    def format_currency_axis(ax, axis: str = 'y'):              # format axis to display currency values
        if axis == 'y':
            ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        else:
            ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))

    @staticmethod
    def add_recession_shading(ax, start_dates: List[str], end_dates: List[str]):        # add recession period shading to plots.  
        for start, end in zip(start_dates, end_dates):
            ax.axvspan(pd.to_datetime(start), pd.to_datetime(end), 
                      alpha=0.2, color='gray', label='Recession')  


    @staticmethod
    def save_plot(fig, filename: str, directory: str = 'static/images'):            # aave plot to specified directory.
        import os
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        fig.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {filepath}")  
    


    

