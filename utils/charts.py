"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Chart Utilities

DESCRIPTION
    Centralized Plotly chart library used throughout the application.

    This module provides reusable chart functions that maintain a
    consistent appearance across all pages of KEIAP.

SUPPORTED CHARTS

    • Horizontal Bar Chart
    • Vertical Bar Chart
    • Donut Chart
    • Pie Chart
    • Histogram
    • Box Plot
    • Scatter Plot
    • Line Chart
    • Treemap
    • Sunburst Chart
    • Empty Chart

AUTHOR
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# IMPORTS
# =============================================================================

import pandas as pd

import plotly.express as px
import plotly.graph_objects as go

# =============================================================================
# KEIAP COLOUR PALETTE
# =============================================================================

PRIMARY = "#1D4ED8"
SECONDARY = "#64748B"

SUCCESS = "#16A34A"
WARNING = "#F59E0B"
DANGER = "#DC2626"

BACKGROUND = "#FFFFFF"
GRID = "#E5E7EB"
TEXT = "#111827"

# Sequential palette

BLUES = [
    "#DBEAFE",
    "#BFDBFE",
    "#93C5FD",
    "#60A5FA",
    "#3B82F6",
    "#2563EB",
    "#1D4ED8",
]

# =============================================================================
# GLOBAL THEME
# =============================================================================


def apply_theme(fig: go.Figure) -> go.Figure:
    """
    Apply the KEIAP plotting theme.

    Parameters
    ----------
    fig : plotly.graph_objects.Figure

    Returns
    -------
    plotly.graph_objects.Figure
    """

    fig.update_layout(

        template="plotly_white",

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

        font=dict(

            family="Arial",

            size=13,

            color=TEXT,

        ),

        title=dict(

            x=0.02,

            xanchor="left",

            font=dict(

                size=20,

                color=TEXT,

            ),

        ),

        margin=dict(

            l=40,
            r=30,
            t=70,
            b=40,

        ),

        legend=dict(

            orientation="h",

            y=1.08,

            x=0,

        ),

        hoverlabel=dict(

            bgcolor="white",

            font_size=13,

        ),

    )

    fig.update_xaxes(

        showgrid=False,

        zeroline=False,

    )

    fig.update_yaxes(

        gridcolor=GRID,

        zeroline=False,

    )

    return fig


# =============================================================================
# EMPTY CHART
# =============================================================================


def empty_chart(message: str = "No data available") -> go.Figure:
    """
    Return an empty placeholder chart.

    Parameters
    ----------
    message : str
        Message displayed in the centre of the chart.
    """

    fig = go.Figure()

    fig.add_annotation(

        text=message,

        x=0.5,

        y=0.5,

        showarrow=False,

        font=dict(

            size=18,

            color=SECONDARY,

        ),

    )

    fig.update_xaxes(visible=False)

    fig.update_yaxes(visible=False)

    fig.update_layout(

        height=400,

        paper_bgcolor=BACKGROUND,

        plot_bgcolor=BACKGROUND,

    )

    return fig


# =============================================================================
# HORIZONTAL BAR CHART
# =============================================================================


def horizontal_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    colour: str = PRIMARY,
) -> go.Figure:
    """
    Create a horizontal bar chart.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str
        Numerical column.

    y : str
        Category column.

    title : str

    colour : str
    """

    if df.empty:

        return empty_chart()

    fig = px.bar(

        df,

        x=x,

        y=y,

        orientation="h",

        title=title,

        color_discrete_sequence=[colour],

        text=x,

    )

    fig.update_traces(

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=(
            "<b>%{y}</b>"
            "<br>%{x:,}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        height=550,

    )

    return apply_theme(fig)


# =============================================================================
# VERTICAL BAR CHART
# =============================================================================


def vertical_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    colour: str = PRIMARY,
) -> go.Figure:
    """
    Create a vertical bar chart.
    """

    if df.empty:

        return empty_chart()

    fig = px.bar(

        df,

        x=x,

        y=y,

        title=title,

        color_discrete_sequence=[colour],

        text=y,

    )

    fig.update_traces(

        texttemplate="%{text:,}",

        textposition="outside",

        hovertemplate=(
            "<b>%{x}</b>"
            "<br>%{y:,}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        height=500,

    )

    return apply_theme(fig)
# =============================================================================
# DONUT CHART
# =============================================================================

def donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
) -> go.Figure:
    """
    Create a donut chart for displaying proportional data.

    Parameters
    ----------
    df : pandas.DataFrame

    names : str
        Column containing category names.

    values : str
        Column containing numerical values.

    title : str
        Chart title.
    """

    if df.empty:

        return empty_chart()

    fig = px.pie(

        df,

        names=names,

        values=values,

        hole=0.55,

        title=title,

        color_discrete_sequence=BLUES,

    )

    fig.update_traces(

        textinfo="percent+label",

        textposition="inside",

        hovertemplate=(
            "<b>%{label}</b>"
            "<br>%{value:,}"
            "<br>%{percent}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        height=500,

    )

    return apply_theme(fig)


# =============================================================================
# PIE CHART
# =============================================================================

def pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
) -> go.Figure:
    """
    Create a standard pie chart.
    """

    if df.empty:

        return empty_chart()

    fig = px.pie(

        df,

        names=names,

        values=values,

        title=title,

        color_discrete_sequence=BLUES,

    )

    fig.update_traces(

        textinfo="percent+label",

        textposition="inside",

        hovertemplate=(
            "<b>%{label}</b>"
            "<br>%{value:,}"
            "<br>%{percent}"
            "<extra></extra>"
        ),

    )

    fig.update_layout(

        height=500,

    )

    return apply_theme(fig)


# =============================================================================
# HISTOGRAM
# =============================================================================

def histogram(
    df: pd.DataFrame,
    column: str,
    title: str,
    bins: int = 30,
) -> go.Figure:
    """
    Create a histogram showing the distribution of a numeric variable.
    """

    if df.empty:

        return empty_chart()

    fig = px.histogram(

        df,

        x=column,

        nbins=bins,

        title=title,

        color_discrete_sequence=[PRIMARY],

    )

    fig.update_layout(

        bargap=0.05,

        height=500,

    )

    fig.update_traces(

        hovertemplate=(
            "<b>Count</b>: %{y}"
            "<br>Value: %{x}"
            "<extra></extra>"
        ),

    )

    return apply_theme(fig)


# =============================================================================
# BOX PLOT
# =============================================================================

def box_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
) -> go.Figure:
    """
    Create a box plot for comparing distributions.
    """

    if df.empty:

        return empty_chart()

    fig = px.box(

        df,

        x=x,

        y=y,

        title=title,

        color=x,

        color_discrete_sequence=BLUES,

        points="outliers",

    )

    fig.update_layout(

        showlegend=False,

        height=550,

    )

    fig.update_traces(

        hovertemplate=(
            "<b>%{x}</b>"
            "<br>Value: %{y:,}"
            "<extra></extra>"
        ),

    )

    return apply_theme(fig)
# =============================================================================
# SCATTER PLOT
# =============================================================================

def scatter_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    colour: str | None = None,
    size: str | None = None,
) -> go.Figure:
    """
    Create an interactive scatter plot.

    Parameters
    ----------
    df : pandas.DataFrame

    x : str
        X-axis column.

    y : str
        Y-axis column.

    colour : str, optional
        Column used to colour the points.

    size : str, optional
        Column used to size the points.
    """

    if df.empty:

        return empty_chart()

    fig = px.scatter(

        df,

        x=x,

        y=y,

        color=colour,

        size=size,

        title=title,

        color_continuous_scale="Blues",

    )

    fig.update_layout(

        height=550,

    )

    fig.update_traces(

        marker=dict(

            opacity=0.8,

            line=dict(

                width=0.5,

                color="white",

            ),

        )

    )

    return apply_theme(fig)


# =============================================================================
# LINE CHART
# =============================================================================

def line_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    colour: str = PRIMARY,
) -> go.Figure:
    """
    Create a line chart.
    """

    if df.empty:

        return empty_chart()

    fig = px.line(

        df,

        x=x,

        y=y,

        title=title,

    )

    fig.update_traces(

        line=dict(

            color=colour,

            width=3,

        ),

        mode="lines+markers",

    )

    fig.update_layout(

        height=500,

    )

    return apply_theme(fig)


# =============================================================================
# TREEMAP
# =============================================================================

def treemap(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    title: str,
) -> go.Figure:
    """
    Create a treemap visualization.
    """

    if df.empty:

        return empty_chart()

    fig = px.treemap(

        df,

        path=path,

        values=values,

        title=title,

        color=values,

        color_continuous_scale="Blues",

    )

    fig.update_layout(

        height=650,

    )

    return apply_theme(fig)


# =============================================================================
# SUNBURST CHART
# =============================================================================

def sunburst_chart(
    df: pd.DataFrame,
    path: list[str],
    values: str,
    title: str,
) -> go.Figure:
    """
    Create a sunburst chart.
    """

    if df.empty:

        return empty_chart()

    fig = px.sunburst(

        df,

        path=path,

        values=values,

        title=title,

        color=values,

        color_continuous_scale="Blues",

    )

    fig.update_layout(

        height=650,

    )

    return apply_theme(fig)