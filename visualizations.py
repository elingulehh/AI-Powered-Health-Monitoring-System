import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def create_multi_user_time_series(df, metric='heart_rate', anomaly_col='anomaly', title=None):
    """Create interactive Plotly time series for multiple users with anomaly highlighting"""
    fig = go.Figure()
    
    if 'user_id' in df.columns:
        users = df['user_id'].unique()
        colors = px.colors.qualitative.Plotly
        
        for i, user in enumerate(users):
            user_df = df[df['user_id'] == user]
            color = colors[i % len(colors)]
            
            # Normal data
            normal_data = user_df[user_df[anomaly_col] == 'Normal'] if anomaly_col in user_df.columns else user_df
            fig.add_trace(go.Scatter(
                x=normal_data['timestamp'],
                y=normal_data[metric],
                mode='lines',
                name=f'{user} (Normal)',
                line=dict(color=color),
                hovertemplate=f'{user}<br>Time: %{{x}}<br>{metric}: %{{y}}<extra></extra>'
            ))
            
            # Anomaly data
            if anomaly_col in user_df.columns:
                anomaly_data = user_df[user_df[anomaly_col] == 'Anomaly']
                if not anomaly_data.empty:
                    fig.add_trace(go.Scatter(
                        x=anomaly_data['timestamp'],
                        y=anomaly_data[metric],
                        mode='markers',
                        name=f'{user} (Anomaly)',
                        marker=dict(color='red', size=10, symbol='x'),
                        hovertemplate=f'{user} ANOMALY<br>Time: %{{x}}<br>{metric}: %{{y}}<extra></extra>'
                    ))
    else:
        # Single user
        normal_data = df[df[anomaly_col] == 'Normal'] if anomaly_col in df.columns else df
        fig.add_trace(go.Scatter(
            x=normal_data['timestamp'],
            y=normal_data[metric],
            mode='lines',
            name='Normal',
            line=dict(color='blue')
        ))
        
        if anomaly_col in df.columns:
            anomaly_data = df[df[anomaly_col] == 'Anomaly']
            if not anomaly_data.empty:
                fig.add_trace(go.Scatter(
                    x=anomaly_data['timestamp'],
                    y=anomaly_data[metric],
                    mode='markers',
                    name='Anomaly',
                    marker=dict(color='red', size=10, symbol='x')
                ))
    
    fig.update_layout(
        title=title or f'{metric.replace("_", " ").title()} Over Time',
        xaxis_title='Time',
        yaxis_title=metric.replace('_', ' ').title(),
        hovermode='closest',
        height=500
    )
    
    return fig

def create_multi_metric_dashboard(df, user_id=None):
    """Create 2x2 dashboard with heart rate, blood oxygen, temperature, respiration"""
    metrics = ['heart_rate', 'blood_oxygen', 'temperature', 'respiration_rate']
    titles = ['Heart Rate (BPM)', 'Blood Oxygen (%)', 'Temperature (°C)', 'Respiration Rate']
    
    if user_id and 'user_id' in df.columns:
        df = df[df['user_id'] == user_id]
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=titles,
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]]
    )
    
    colors = ['blue', 'green', 'orange', 'purple']
    
    for idx, (metric, title, color) in enumerate(zip(metrics, titles, colors)):
        if metric in df.columns:
            row = (idx // 2) + 1
            col = (idx % 2) + 1
            
            fig.add_trace(
                go.Scatter(
                    x=df['timestamp'],
                    y=df[metric],
                    mode='lines',
                    name=title,
                    line=dict(color=color),
                    showlegend=False
                ),
                row=row, col=col
            )
    
    fig.update_layout(height=700, showlegend=False, title_text="Health Metrics Dashboard")
    return fig

def create_anomaly_heatmap(df):
    """Create heatmap showing anomaly distribution by user and hour"""
    if 'user_id' not in df.columns or 'anomaly' not in df.columns:
        return None
    
    df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
    
    # Create pivot table
    pivot = df[df['anomaly'] == 'Anomaly'].groupby(['user_id', 'hour']).size().reset_index(name='count')
    pivot_table = pivot.pivot(index='user_id', columns='hour', values='count').fillna(0)
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_table.values,
        x=pivot_table.columns,
        y=pivot_table.index,
        colorscale='Reds',
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='Anomaly Distribution by User and Hour',
        xaxis_title='Hour of Day',
        yaxis_title='User ID',
        height=400
    )
    
    return fig

def create_correlation_matrix(df):
    """Create correlation heatmap for health metrics"""
    metrics = ['heart_rate', 'blood_oxygen', 'temperature', 'respiration_rate']
    available_metrics = [m for m in metrics if m in df.columns]
    
    if len(available_metrics) < 2:
        return None
    
    corr = df[available_metrics].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=[m.replace('_', ' ').title() for m in corr.columns],
        y=[m.replace('_', ' ').title() for m in corr.index],
        colorscale='RdBu',
        zmid=0,
        text=corr.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title='Health Metrics Correlation Matrix',
        height=500
    )
    
    return fig

def create_distribution_plots(df, metric='heart_rate'):
    """Create distribution plot with box plot and histogram"""
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=[f'{metric.replace("_", " ").title()} Distribution', 
                       f'{metric.replace("_", " ").title()} Box Plot']
    )
    
    # Histogram
    fig.add_trace(
        go.Histogram(x=df[metric], name='Distribution', marker_color='skyblue'),
        row=1, col=1
    )
    
    # Box plot
    if 'user_id' in df.columns:
        for user in df['user_id'].unique():
            user_data = df[df['user_id'] == user]
            fig.add_trace(
                go.Box(y=user_data[metric], name=user),
                row=1, col=2
            )
    else:
        fig.add_trace(
            go.Box(y=df[metric], name=metric),
            row=1, col=2
        )
    
    fig.update_layout(height=400, showlegend=True)
    return fig

def create_prediction_comparison(actual, predicted, timestamps, metric='heart_rate'):
    """Create comparison plot for actual vs predicted values"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=actual,
        mode='lines+markers',
        name='Actual',
        line=dict(color='blue'),
        marker=dict(size=6)
    ))
    
    fig.add_trace(go.Scatter(
        x=timestamps,
        y=predicted,
        mode='lines+markers',
        name='Predicted',
        line=dict(color='red', dash='dash'),
        marker=dict(size=6, symbol='diamond')
    ))
    
    fig.update_layout(
        title=f'{metric.replace("_", " ").title()} - Actual vs Predicted',
        xaxis_title='Time',
        yaxis_title=metric.replace('_', ' ').title(),
        hovermode='x unified',
        height=500
    )
    
    return fig

def create_metric_cards_data(df, user_id=None):
    """Calculate metrics for display cards"""
    if user_id and 'user_id' in df.columns:
        df = df[df['user_id'] == user_id]
    
    if df.empty:
        return {}
    
    latest = df.iloc[-1] if not df.empty else {}
    
    metrics = {}
    
    # Heart Rate
    if 'heart_rate' in df.columns:
        hr_mean = df['heart_rate'].mean()
        hr_current = latest.get('heart_rate', 0)
        metrics['heart_rate'] = {
            'current': hr_current,
            'mean': hr_mean,
            'min': df['heart_rate'].min(),
            'max': df['heart_rate'].max(),
            'trend': 'up' if hr_current > hr_mean else 'down'
        }
    
    # Blood Oxygen
    if 'blood_oxygen' in df.columns:
        o2_mean = df['blood_oxygen'].mean()
        o2_current = latest.get('blood_oxygen', 0)
        metrics['blood_oxygen'] = {
            'current': o2_current,
            'mean': o2_mean,
            'min': df['blood_oxygen'].min(),
            'max': df['blood_oxygen'].max(),
            'trend': 'up' if o2_current > o2_mean else 'down'
        }
    
    # Temperature
    if 'temperature' in df.columns:
        temp_mean = df['temperature'].mean()
        temp_current = latest.get('temperature', 0)
        metrics['temperature'] = {
            'current': temp_current,
            'mean': temp_mean,
            'min': df['temperature'].min(),
            'max': df['temperature'].max(),
            'trend': 'up' if temp_current > temp_mean else 'down'
        }
    
    # Anomaly count
    if 'anomaly' in df.columns:
        anomaly_count = len(df[df['anomaly'] == 'Anomaly'])
        metrics['anomalies'] = {
            'count': anomaly_count,
            'percentage': (anomaly_count / len(df) * 100) if len(df) > 0 else 0
        }
    
    return metrics
