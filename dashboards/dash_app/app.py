import dash
from dash import dcc, html, Input, Output, callback, dash_table
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import sys
import os

# Get the absolute path of the project root and add it to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
sys.path.insert(0, project_root)
 
from src.data_collection import FinancialDataCollector
from src.data_processing import FinancialDataProcessor
from src.config import SECTOR_MAPPING

# Load data
collector = FinancialDataCollector()
stock_data = collector.load_stock_data()
processor = FinancialDataProcessor(stock_data)

# Prepare data for the app
master_df = collector.create_master_dataframe(stock_data)
stock_list = list(stock_data.keys())[:20]  # Limit for performance

# Initialize Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Financial Market Analytics Dashboard", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': 30}),
    
    # Navigation tabs
    dcc.Tabs(id="main-tabs", value='overview', children=[
        dcc.Tab(label='Market Overview', value='overview'),
        dcc.Tab(label='Stock Analysis', value='stocks'),
        dcc.Tab(label='Portfolio Builder', value='portfolio'),
        dcc.Tab(label='Risk Analysis', value='risk'),
    ]),
    
    html.Div(id='tab-content')
])

# Overview tab layout
overview_layout = html.Div([
    html.H2("Market Overview", style={'color': '#34495e'}),
    
    html.Div([
        html.Div([
            html.H4("Select Stocks for Comparison:"),
            dcc.Dropdown(
                id='overview-stock-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in stock_list],
                value=['AAPL', 'GOOGL', 'MSFT', 'TSLA'],
                multi=True
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H4("Time Range:"),
            dcc.DatePickerRange(
                id='overview-date-picker',
                start_date=master_df.index.min(),
                end_date=master_df.index.max(),
                display_format='YYYY-MM-DD'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': 20}),
    
    dcc.Graph(id='overview-price-chart'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='overview-correlation-heatmap')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='overview-sector-performance')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
])

# Stock analysis tab layout
stock_analysis_layout = html.Div([
    html.H2("Individual Stock Analysis", style={'color': '#34495e'}),
    
    html.Div([
        html.Div([
            html.H4("Select Stock:"),
            dcc.Dropdown(
                id='stock-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in stock_list],
                value='AAPL'
            )
        ], style={'width': '30%', 'display': 'inline-block'}),
        
        html.Div([
            html.H4("Analysis Period:"),
            dcc.RadioItems(
                id='analysis-period',
                options=[
                    {'label': '3 Months', 'value': 90},
                    {'label': '6 Months', 'value': 180},
                    {'label': '1 Year', 'value': 365},
                    {'label': 'All Time', 'value': 999}
                ],
                value=365,
                inline=True
            )
        ], style={'width': '40%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': 20}),
    
    # Stock metrics cards
    html.Div(id='stock-metrics-cards', style={'marginBottom': 20}),
    
    dcc.Graph(id='stock-price-volume-chart'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='stock-returns-distribution')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='stock-technical-indicators')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
])

# Portfolio builder tab layout
portfolio_layout = html.Div([
    html.H2("Portfolio Builder & Optimizer", style={'color': '#34495e'}),
    
    html.Div([
        html.Div([
            html.H4("Build Your Portfolio:"),
            html.Div(id='portfolio-builder')
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.H4("Portfolio Metrics:"),
            html.Div(id='portfolio-metrics')
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': 20}),
    
    dcc.Graph(id='portfolio-performance-chart'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='portfolio-allocation-pie')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='efficient-frontier')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
])

# Risk analysis tab layout
risk_analysis_layout = html.Div([
    html.H2("Risk Analysis Dashboard", style={'color': '#34495e'}),
    
    html.Div([
        html.Div([
            html.H4("Select Stocks for Risk Analysis:"),
            dcc.Dropdown(
                id='risk-stock-dropdown',
                options=[{'label': ticker, 'value': ticker} for ticker in stock_list],
                value=['AAPL', 'TSLA', 'NVDA', 'AMD'],
                multi=True
            )
        ], style={'width': '60%', 'display': 'inline-block'}),
        
        html.Div([
            html.H4("Risk Metric:"),
            dcc.RadioItems(
                id='risk-metric',
                options=[
                    {'label': 'Volatility', 'value': 'volatility'},
                    {'label': 'VaR 95%', 'value': 'var_95'},
                    {'label': 'Max Drawdown', 'value': 'max_drawdown'}
                ],
                value='volatility',
                inline=True
            )
        ], style={'width': '35%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': 20}),
    
    dcc.Graph(id='risk-return-scatter'),
    
    html.Div([
        html.Div([
            dcc.Graph(id='volatility-clustering')
        ], style={'width': '50%', 'display': 'inline-block'}),
        
        html.Div([
            dcc.Graph(id='risk-metrics-table')
        ], style={'width': '50%', 'float': 'right', 'display': 'inline-block'})
    ])
])

# Callback for tab content
@app.callback(Output('tab-content', 'children'),
              Input('main-tabs', 'value'))
def render_content(tab):
    if tab == 'overview':
        return overview_layout
    elif tab == 'stocks':
        return stock_analysis_layout
    elif tab == 'portfolio':
        return portfolio_layout
    elif tab == 'risk':
        return risk_analysis_layout

# Overview callbacks
@app.callback(
    [Output('overview-price-chart', 'figure'),
     Output('overview-correlation-heatmap', 'figure'),
     Output('overview-sector-performance', 'figure')],
    [Input('overview-stock-dropdown', 'value'),
     Input('overview-date-picker', 'start_date'),
     Input('overview-date-picker', 'end_date')]
)
def update_overview_charts(selected_stocks, start_date, end_date):
    # Filter data
    filtered_df = master_df.loc[start_date:end_date, selected_stocks]
    
    # Normalize prices
    normalized_df = filtered_df / filtered_df.iloc[0] * 100
    
    # Price comparison chart
    price_fig = go.Figure()
    for stock in selected_stocks:
        price_fig.add_trace(go.Scatter(
            x=normalized_df.index,
            y=normalized_df[stock],
            mode='lines',
            name=stock,
            line=dict(width=2)
        ))
    
    price_fig.update_layout(
        title='Normalized Stock Price Comparison (Base=100)',
        xaxis_title='Date',
        yaxis_title='Normalized Price',
        hovermode='x unified'
    )
    
    # Correlation heatmap
    correlation_matrix = processor.calculate_correlation_matrix(selected_stocks)
    corr_fig = go.Figure(data=go.Heatmap(
        z=correlation_matrix.values,
        x=correlation_matrix.columns,
        y=correlation_matrix.index,
        colorscale='RdBu',
        zmid=0
    ))
    corr_fig.update_layout(title='Stock Correlation Matrix')
    
    # Sector performance
    sector_performance = []
    for sector, tickers in SECTOR_MAPPING.items():
        sector_stocks = [t for t in tickers if t in selected_stocks]
        if sector_stocks:
            sector_returns = []
            for ticker in sector_stocks:
                if ticker in stock_data:
                    returns = stock_data[ticker]['prices']['Returns'].dropna()
                    annual_return = returns.mean() * 252 * 100
                    sector_returns.append(annual_return)
            
            if sector_returns:
                sector_performance.append({
                    'Sector': sector,
                    'Average_Return': np.mean(sector_returns),
                    'Count': len(sector_returns)
                })
    
    sector_df = pd.DataFrame(sector_performance)
    sector_fig = px.bar(sector_df, x='Sector', y='Average_Return',
                       title='Average Sector Performance')
    
    return price_fig, corr_fig, sector_fig

# Stock analysis callbacks
@app.callback(
    [Output('stock-metrics-cards', 'children'),
     Output('stock-price-volume-chart', 'figure'),
     Output('stock-returns-distribution', 'figure'),
     Output('stock-technical-indicators', 'figure')],
    [Input('stock-dropdown', 'value'),
     Input('analysis-period', 'value')]
)
def update_stock_analysis(selected_stock, period_days):
    if selected_stock not in stock_data:
        return [], {}, {}, {}
    
    # Get stock data
    prices = stock_data[selected_stock]['prices']
    if period_days < 999:
        prices = prices.tail(period_days)
    
    # Calculate metrics
    returns = prices['Returns'].dropna() * 100
    annual_return = returns.mean() * 252
    annual_volatility = returns.std() * np.sqrt(252)
    sharpe_ratio = annual_return / annual_volatility if annual_volatility != 0 else 0
    
    # Metrics cards
    metrics_cards = html.Div([
        html.Div([
            html.H4(f"{annual_return:.1f}%", style={'color': '#27ae60', 'margin': 0}),
            html.P("Annual Return", style={'margin': 0})
        ], className='metric-card', style={'display': 'inline-block', 'margin': '10px', 
                                         'padding': '15px', 'border': '1px solid #ddd',
                                         'borderRadius': '5px', 'textAlign': 'center'}),
        
        html.Div([
            html.H4(f"{annual_volatility:.1f}%", style={'color': '#e74c3c', 'margin': 0}),
            html.P("Annual Volatility", style={'margin': 0})
        ], className='metric-card', style={'display': 'inline-block', 'margin': '10px',
                                         'padding': '15px', 'border': '1px solid #ddd',
                                         'borderRadius': '5px', 'textAlign': 'center'}),
        
        html.Div([
            html.H4(f"{sharpe_ratio:.2f}", style={'color': '#3498db', 'margin': 0}),
            html.P("Sharpe Ratio", style={'margin': 0})
        ], className='metric-card', style={'display': 'inline-block', 'margin': '10px',
                                         'padding': '15px', 'border': '1px solid #ddd',
                                         'borderRadius': '5px', 'textAlign': 'center'})
    ])
    
    # Price and volume chart
    price_volume_fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=('Stock Price', 'Volume'),
        row_width=[0.7, 0.3]
    )
    
    price_volume_fig.add_trace(
        go.Scatter(x=prices.index, y=prices['Close'], name='Price', line=dict(width=2)),
        row=1, col=1
    )
    
    price_volume_fig.add_trace(
        go.Bar(x=prices.index, y=prices['Volume'], name='Volume', marker_color='lightblue'),
        row=2, col=1
    )
    
    price_volume_fig.update_layout(title=f'{selected_stock} - Price and Volume Analysis')
    
    # Returns distribution
    returns_fig = go.Figure()
    returns_fig.add_trace(go.Histogram(x=returns, nbinsx=50, name='Returns Distribution'))
    returns_fig.update_layout(
        title=f'{selected_stock} - Daily Returns Distribution',
        xaxis_title='Daily Returns (%)',
        yaxis_title='Frequency'
    )
    
    # Technical indicators
    tech_fig = go.Figure()
    tech_fig.add_trace(go.Scatter(x=prices.index, y=prices['Close'], name='Price'))
    tech_fig.add_trace(go.Scatter(x=prices.index, y=prices['MA_20'], name='MA 20'))
    tech_fig.add_trace(go.Scatter(x=prices.index, y=prices['MA_50'], name='MA 50'))
    tech_fig.update_layout(title=f'{selected_stock} - Technical Indicators')
    
    return metrics_cards, price_volume_fig, returns_fig, tech_fig

# Portfolio builder callbacks
@app.callback(
    [Output('portfolio-builder', 'children'),
     Output('portfolio-metrics', 'children'),
     Output('portfolio-performance-chart', 'figure'),
     Output('portfolio-allocation-pie', 'figure'),
     Output('efficient-frontier', 'figure')],
    [Input('main-tabs', 'value')]  # Trigger on tab change
)
def update_portfolio_tab(tab_value):
    if tab_value != 'portfolio':
        return [], [], {}, {}, {}
    
    # Default portfolio
    default_stocks = ['AAPL', 'GOOGL', 'MSFT', 'AMZN', 'TSLA']
    default_weights = [0.3, 0.25, 0.2, 0.15, 0.1]
    
    # Portfolio builder components
    builder_components = []
    for i, stock in enumerate(default_stocks):
        builder_components.extend([
            html.Div([
                html.Label(f'{stock}:'),
                dcc.Slider(
                    id=f'weight-{stock}',
                    min=0, max=1, step=0.05,
                    value=default_weights[i],
                    marks={i/10: f'{i/10:.1f}' for i in range(0, 11, 2)},
                    tooltip={'placement': 'bottom'}
                )
            ], style={'marginBottom': '10px'})
        ])
    
    portfolio_builder = html.Div(builder_components)
    
    # Calculate portfolio metrics
    portfolio_metrics_calc = processor.calculate_portfolio_metrics(default_stocks, default_weights)
    
    portfolio_metrics = html.Div([
        html.P(f"Annual Return: {portfolio_metrics_calc['annual_return']:.2%}"),
        html.P(f"Annual Volatility: {portfolio_metrics_calc['annual_volatility']:.2%}"),
        html.P(f"Sharpe Ratio: {portfolio_metrics_calc['sharpe_ratio']:.2f}"),
        html.P(f"Total Return: {portfolio_metrics_calc['total_return']:.2%}"),
        html.P(f"Max Drawdown: {portfolio_metrics_calc['max_drawdown']:.2%}")
    ])
    
    # Portfolio performance chart
    portfolio_returns = portfolio_metrics_calc['returns']
    cumulative_returns = (1 + portfolio_returns).cumprod()
    
    perf_fig = go.Figure()
    perf_fig.add_trace(go.Scatter(
        x=cumulative_returns.index,
        y=cumulative_returns.values,
        mode='lines',
        name='Portfolio Performance'
    ))
    perf_fig.update_layout(title='Portfolio Cumulative Performance')
    
    # Allocation pie chart
    allocation_fig = go.Figure(data=[go.Pie(
        labels=default_stocks,
        values=default_weights,
        hole=.3
    )])
    allocation_fig.update_layout(title='Portfolio Allocation')
    
    # Efficient frontier (simplified)
    efficient_frontier_fig = go.Figure()
    # This would require more complex optimization - showing placeholder
    efficient_frontier_fig.add_trace(go.Scatter(
        x=[portfolio_metrics_calc['annual_volatility']],
        y=[portfolio_metrics_calc['annual_return']],
        mode='markers',
        marker=dict(size=10, color='red'),
        name='Current Portfolio'
    ))
    efficient_frontier_fig.update_layout(
        title='Efficient Frontier',
        xaxis_title='Volatility',
        yaxis_title='Expected Return'
    )
    
    return portfolio_builder, portfolio_metrics, perf_fig, allocation_fig, efficient_frontier_fig

# Risk analysis callbacks
@app.callback(
    [Output('risk-return-scatter', 'figure'),
     Output('volatility-clustering', 'figure'),
     Output('risk-metrics-table', 'figure')],
    [Input('risk-stock-dropdown', 'value'),
     Input('risk-metric', 'value')]
)
def update_risk_analysis(selected_stocks, risk_metric):
    if not selected_stocks:
        return {}, {}, {}
    
    # Risk-return scatter
    risk_return_data = []
    for ticker in selected_stocks:
        if ticker in stock_data:
            returns = stock_data[ticker]['prices']['Returns'].dropna()
            annual_return = returns.mean() * 252 * 100
            annual_volatility = returns.std() * np.sqrt(252) * 100
            
            risk_return_data.append({
                'Stock': ticker,
                'Return': annual_return,
                'Volatility': annual_volatility
            })
    
    rr_df = pd.DataFrame(risk_return_data)
    
    scatter_fig = px.scatter(
        rr_df, x='Volatility', y='Return',
        text='Stock', title='Risk vs Return Analysis'
    )
    scatter_fig.update_traces(textposition="top center")
    
    # Volatility clustering for first stock
    first_stock = selected_stocks[0]
    returns = stock_data[first_stock]['prices']['Returns'].dropna() * 100
    rolling_vol = returns.rolling(window=30).std()
    
    vol_fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
    vol_fig.add_trace(go.Scatter(x=returns.index, y=returns, name='Returns'), row=1, col=1)
    vol_fig.add_trace(go.Scatter(x=rolling_vol.index, y=rolling_vol, name='Rolling Vol'), row=2, col=1)
    vol_fig.update_layout(title=f'{first_stock} - Volatility Clustering')
    
    # Risk metrics table
    risk_data = []
    for stock in selected_stocks:
        if stock in stock_data:
            risk_metrics = processor.calculate_risk_metrics(stock)
            risk_data.append({
                'Stock': stock,
                'Volatility': f"{risk_metrics.get('volatility', 0)*100:.1f}%",
                'VaR 95%': f"{risk_metrics.get('var_95', 0)*100:.2f}%",
                'Max Loss': f"{risk_metrics.get('max_daily_loss', 0)*100:.2f}%"
            })
    
    risk_table_fig = go.Figure(data=[go.Table(
        header=dict(values=list(risk_data[0].keys())),
        cells=dict(values=[[row[col] for row in risk_data] for col in risk_data[0].keys()])
    )])
    risk_table_fig.update_layout(title='Risk Metrics Summary')
    
    return scatter_fig, vol_fig, risk_table_fig

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)

# change the directory to dash_app and run app.py. Check the portal http://127.0.0.1:8050/ for the visualization
