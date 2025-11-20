"""
HealthScope Chart Utilities
Animated Plotly charts with theme-specific styling
"""

import plotly.graph_objects as go
import plotly.express as px
from utils.themes import HealthScopeTheme as Theme
import pandas as pd
import numpy as np


def create_pie_chart(data, labels, title, theme='home'):
    """
    Create an animated pie chart
    
    Args:
        data: Values for pie chart
        labels: Labels for each slice
        title: Chart title
        theme: Color theme
    """
    theme_colors = getattr(Theme, 'CHART_COLORS', Theme.CHART_COLORS)[theme]
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=data,
        hole=0.4,
        marker=dict(colors=theme_colors, line=dict(color='white', width=2)),
        textinfo='percent+label',
        textfont=dict(size=14, family=Theme.FONT_FAMILY),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5),
        height=400,
        margin=dict(t=80, b=60, l=40, r=40),
        transition={'duration': 500}
    )
    
    return fig


def create_histogram(data, column, title, theme='home', nbins=30):
    """
    Create an animated histogram
    
    Args:
        data: DataFrame with data
        column: Column name to plot
        title: Chart title
        theme: Color theme
        nbins: Number of bins
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    
    fig = go.Figure(data=[go.Histogram(
        x=data[column],
        nbinsx=nbins,
        marker=dict(
            color=theme_obj['primary'],
            line=dict(color='white', width=1)
        ),
        name=column,
        hovertemplate='<b>Range:</b> %{x}<br><b>Count:</b> %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='Frequency',
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        bargap=0.1,
        height=400,
        margin=dict(t=80, b=60, l=60, r=40),
        transition={'duration': 500}
    )
    
    return fig


def create_boxplot(data, column, title, theme='home'):
    """
    Create an animated box plot
    
    Args:
        data: DataFrame with data
        column: Column name to plot
        title: Chart title
        theme: Color theme
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    
    fig = go.Figure(data=[go.Box(
        y=data[column],
        name=column,
        marker=dict(color=theme_obj['primary']),
        boxmean='sd',
        hovertemplate='<b>Value:</b> %{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        yaxis=dict(
            title=column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        height=400,
        margin=dict(t=80, b=60, l=60, r=40),
        showlegend=False,
        transition={'duration': 500}
    )
    
    return fig


def create_correlation_heatmap(data, title, theme='home'):
    """
    Create a correlation heatmap
    
    Args:
        data: DataFrame with numeric columns
        title: Chart title
        theme: Color theme
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    
    # Calculate correlation matrix
    corr_matrix = data.select_dtypes(include=[np.number]).corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale=[[0, 'white'], [0.5, theme_obj['primary']], [1, theme_obj['secondary']]],
        text=np.round(corr_matrix.values, 2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlation"),
        hovertemplate='<b>%{x}</b> vs <b>%{y}</b><br>Correlation: %{z:.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=500,
        margin=dict(t=80, b=100, l=100, r=40),
        xaxis=dict(side='bottom', tickangle=-45),
        yaxis=dict(autorange='reversed'),
        transition={'duration': 500}
    )
    
    return fig


def create_feature_importance_chart(feature_names, importance_values, title, theme='home', top_n=10):
    """
    Create a feature importance bar chart
    
    Args:
        feature_names: List of feature names
        importance_values: List of importance values
        title: Chart title
        theme: Color theme
        top_n: Number of top features to show
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    
    # Sort and get top N features
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance_values
    }).sort_values('importance', ascending=False).head(top_n)
    
    fig = go.Figure(data=[go.Bar(
        x=importance_df['importance'],
        y=importance_df['feature'],
        orientation='h',
        marker=dict(
            color=importance_df['importance'],
            colorscale=[[0, theme_obj['primary']], [1, theme_obj['secondary']]],
            line=dict(color='white', width=1)
        ),
        text=np.round(importance_df['importance'], 3),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.4f}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        xaxis=dict(
            title='Importance Score',
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title='',
            autorange='reversed'
        ),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        height=400,
        margin=dict(t=80, b=60, l=150, r=100),
        transition={'duration': 500}
    )
    
    return fig


def create_sparkline_data(data, column, num_points=10):
    """
    Generate sparkline data from a column
    
    Args:
        data: DataFrame
        column: Column to extract data from
        num_points: Number of points to sample
    
    Returns:
        List of values for sparkline
    """
    if len(data) < num_points:
        return data[column].tolist()
    
    # Sample evenly across the data
    indices = np.linspace(0, len(data) - 1, num_points, dtype=int)
    return data[column].iloc[indices].tolist()


def create_bar_chart(data, x_column, y_column, title, theme='home'):
    """
    Create an animated bar chart
    
    Args:
        data: DataFrame with data
        x_column: Column for x-axis
        y_column: Column for y-axis
        title: Chart title
        theme: Color theme
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    
    fig = go.Figure(data=[go.Bar(
        x=data[x_column],
        y=data[y_column],
        marker=dict(
            color=theme_obj['primary'],
            line=dict(color='white', width=1)
        ),
        hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=x_column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=False,
            zeroline=False
        ),
        yaxis=dict(
            title=y_column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        height=400,
        margin=dict(t=80, b=60, l=60, r=40),
        transition={'duration': 500}
    )
    
    return fig


def create_scatter_plot(data, x_column, y_column, title, theme='home', color_column=None):
    """
    Create an animated scatter plot
    
    Args:
        data: DataFrame with data
        x_column: Column for x-axis
        y_column: Column for y-axis
        title: Chart title
        theme: Color theme
        color_column: Optional column for color coding
    """
    theme_obj = getattr(Theme, theme.upper(), Theme.HOME)
    theme_colors = Theme.CHART_COLORS[theme]
    
    if color_column:
        fig = px.scatter(
            data,
            x=x_column,
            y=y_column,
            color=color_column,
            color_discrete_sequence=theme_colors,
            hover_data=data.columns
        )
    else:
        fig = go.Figure(data=[go.Scatter(
            x=data[x_column],
            y=data[y_column],
            mode='markers',
            marker=dict(
                size=8,
                color=theme_obj['primary'],
                line=dict(width=1, color='white')
            ),
            hovertemplate='<b>%{x}</b><br>%{y}<extra></extra>'
        )])
    
    fig.update_layout(
        title=dict(text=title, font=dict(size=20, family=Theme.FONT_FAMILY, color='#1F2937'), x=0.5, xanchor='center'),
        xaxis=dict(
            title=x_column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        yaxis=dict(
            title=y_column,
            gridcolor='rgba(0,0,0,0.05)',
            showgrid=True,
            zeroline=False
        ),
        font=dict(family=Theme.FONT_FAMILY),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.9)',
        height=400,
        margin=dict(t=80, b=60, l=60, r=40),
        transition={'duration': 500}
    )
    
    return fig
