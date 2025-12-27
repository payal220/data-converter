import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import os

OUTPUT_FOLDER = 'outputs'

def generate_visualizations(df, timestamp):
    """Generate multiple visualization options from DataFrame"""
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    
    charts = {}
    
    # Detect column types
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    if len(numeric_cols) == 0:
        # Try to convert first non-object column
        for col in df.columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
                categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
                break
            except:
                pass
    
    # Generate different chart types
    if len(numeric_cols) > 0:
        x_col = categorical_cols[0] if categorical_cols else df.columns[0]
        y_col = numeric_cols[0]
        
        # Bar Chart
        charts['bar'] = create_bar_chart(df, x_col, y_col, timestamp)
        
        # Line Chart
        charts['line'] = create_line_chart(df, x_col, y_col, timestamp)
        
        # Pie Chart (if suitable)
        if len(df) <= 10:
            charts['pie'] = create_pie_chart(df, x_col, y_col, timestamp)
        
        # Scatter Plot (if multiple numeric columns)
        if len(numeric_cols) >= 2:
            charts['scatter'] = create_scatter_plot(df, numeric_cols[0], numeric_cols[1], timestamp)
        
        # Heatmap (if multiple numeric columns)
        if len(numeric_cols) >= 2:
            charts['heatmap'] = create_heatmap(df, timestamp)
    
    return charts

def create_bar_chart(df, x_col, y_col, timestamp):
    """Create an interactive bar chart"""
    fig = go.Figure(data=[
        go.Bar(
            x=df[x_col],
            y=df[y_col],
            marker=dict(
                color=df[y_col],
                colorscale='Viridis',
                showscale=True
            ),
            text=df[y_col],
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title=f'{y_col} by {x_col}',
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        hovermode='x unified',
        height=500
    )
    
    filename = f'{timestamp}_bar_chart.html'
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    fig.write_html(filepath)
    
    return {
        'type': 'bar',
        'filename': filename,
        'html': fig.to_html(include_plotlyjs='cdn', div_id='bar-chart')
    }

def create_line_chart(df, x_col, y_col, timestamp):
    """Create an interactive line chart"""
    fig = go.Figure(data=[
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='lines+markers',
            marker=dict(size=8, color='royalblue'),
            line=dict(width=3, color='royalblue'),
            name=y_col
        )
    ])
    
    fig.update_layout(
        title=f'{y_col} Trend',
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        hovermode='x unified',
        height=500
    )
    
    filename = f'{timestamp}_line_chart.html'
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    fig.write_html(filepath)
    
    return {
        'type': 'line',
        'filename': filename,
        'html': fig.to_html(include_plotlyjs='cdn', div_id='line-chart')
    }

def create_pie_chart(df, label_col, value_col, timestamp):
    """Create an interactive pie chart"""
    fig = go.Figure(data=[
        go.Pie(
            labels=df[label_col],
            values=df[value_col],
            hole=0.3,
            marker=dict(line=dict(color='white', width=2))
        )
    ])
    
    fig.update_layout(
        title=f'{value_col} Distribution',
        template='plotly_white',
        height=500
    )
    
    filename = f'{timestamp}_pie_chart.html'
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    fig.write_html(filepath)
    
    return {
        'type': 'pie',
        'filename': filename,
        'html': fig.to_html(include_plotlyjs='cdn', div_id='pie-chart')
    }

def create_scatter_plot(df, x_col, y_col, timestamp):
    """Create an interactive scatter plot"""
    fig = go.Figure(data=[
        go.Scatter(
            x=df[x_col],
            y=df[y_col],
            mode='markers',
            marker=dict(
                size=12,
                color=df[y_col],
                colorscale='Viridis',
                showscale=True,
                line=dict(width=1, color='white')
            ),
            text=df.index,
            hovertemplate='<b>%{text}</b><br>' +
                         f'{x_col}: %{{x}}<br>' +
                         f'{y_col}: %{{y}}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=f'{y_col} vs {x_col}',
        xaxis_title=x_col,
        yaxis_title=y_col,
        template='plotly_white',
        height=500
    )
    
    filename = f'{timestamp}_scatter_plot.html'
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    fig.write_html(filepath)
    
    return {
        'type': 'scatter',
        'filename': filename,
        'html': fig.to_html(include_plotlyjs='cdn', div_id='scatter-chart')
    }

def create_heatmap(df, timestamp):
    """Create a heatmap for numeric columns"""
    numeric_df = df.select_dtypes(include=['number'])
    
    if numeric_df.empty or len(numeric_df.columns) < 2:
        return None
    
    # Calculate correlation matrix
    corr_matrix = numeric_df.corr()
    
    fig = go.Figure(data=[
        go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            hovertemplate='%{x} vs %{y}<br>Correlation: %{z:.2f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title='Correlation Heatmap',
        template='plotly_white',
        width=600,
        height=600
    )
    
    filename = f'{timestamp}_heatmap.html'
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    fig.write_html(filepath)
    
    return {
        'type': 'heatmap',
        'filename': filename,
        'html': fig.to_html(include_plotlyjs='cdn', div_id='heatmap-chart')
    }