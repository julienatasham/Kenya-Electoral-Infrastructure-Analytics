"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE
    Chart Utilities

DESCRIPTION
    Centralized Plotly chart library used throughout the KEIAP platform.

    All visualizations share a common theme, colour palette and styling
    to ensure consistency across dashboards.

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

PRIMARY = "#0B5ED7"
SECONDARY = "#6C757D"
SUCCESS = "#198754"
WARNING = "#FFC107"
DANGER = "#DC3545"
LIGHT = "#F8F9FA"

BLUES = px.colors.sequential.Blues

# =============================================================================
# GLOBAL SETTINGS
# =============================================================================

CHART_HEIGHT = 500

FONT = dict(
    family="Arial",
    size=13,
    color="#212529",
)

TITLE_FONT = dict(
    family="Arial",
    size=20,
    color="#212529",
)

# =============================================================================
# SHARED THEME
# =============================================================================


def apply_theme(fig: go.Figure) -> go.Figure:
    """
    Apply the KEIAP visual theme to a Plotly figure.
    """

    fig.update_layout(

        template="plotly_white",

        font=FONT,

        title_font=TITLE_FONT,

        height=CHART_HEIGHT,

        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20,
        ),

        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5,
        ),

    )

    return fig


# =============================================================================
# EMPTY CHART
# =============================================================================


def empty_chart(message: str = "No data available") -> go.Figure:
    """
    Return a placeholder chart whenever no data is available.
    """

    fig = go.Figure()

    fig.add_annotation(

        text=message,

        x=0.5,

        y=0.5,

        showarrow=False,

        font=dict(size=18),

    )

    fig.update_xaxes(visible=False)

    fig.update_yaxes(visible=False)

    fig.update_layout(

        template="plotly_white",

        height=CHART_HEIGHT,

    )

    return fig
# =============================================================================
# HORIZONTAL BAR CHART
# =============================================================================

import plotly.express as px


def horizontal_bar_chart(
    df,
    x,
    y,
    title="",
    color=None,
    color_scale="Blues",
):


    fig = px.bar(
        df,
        x=x,
        y=y,
        orientation="h",
        color=color,
        color_continuous_scale=color_scale,
        template="plotly_white",
    )

    fig.update_layout(
        title=title if title else None,
        height=650,
        margin=dict(l=20, r=20, t=60, b=20),
        yaxis=dict(categoryorder="total ascending"),
        title_font=dict(size=22),
    )

    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Registered Voters: %{x:,}<extra></extra>"
    )

    return fig


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

    )

    fig.update_traces(

        hovertemplate="<b>%{x}</b><br>%{y:,.0f}<extra></extra>"

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

    if df.empty:
        return empty_chart()

    # Show only the top 10 categories
    plot_df = df.nlargest(10, values)

    fig = px.pie(

        plot_df,

        names=names,

        values=values,

        hole=0.60,

        title=title,

        color_discrete_sequence=BLUES,

    )

    fig.update_traces(

        textinfo="percent",

        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",

    )

    fig.update_layout(

        legend=dict(

            orientation="v",

            x=1.02,

            y=0.5,

        )

    )

    return apply_theme(fig)

# =============================================================================
# HISTOGRAM
# =============================================================================

def histogram(
    df: pd.DataFrame,
    column: str,
    title: str = "",
) -> go.Figure:
    """
    Create a histogram.
    """

    if df.empty:
        return empty_chart()

    fig = px.histogram(
        df,
        x=column,
        nbins=30,
        template="plotly_white",
        color_discrete_sequence=[PRIMARY],
    )

    fig.update_layout(
        title=title if title else None,
        xaxis_title="Registered Voters",
        yaxis_title="Number of Polling Stations",
        bargap=0.05,
    )

    fig.update_traces(
        opacity=0.85,
        hovertemplate="<b>%{x:,}</b><br>Polling Stations: %{y}<extra></extra>",
    )

    return apply_theme(fig)

# =============================================================================
# BOX PLOT
# =============================================================================

def box_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
) -> go.Figure:
    """
    Create a box plot.
    """

    if df.empty:
        return empty_chart()

    fig = px.box(
        df,
        x=x,
        y=y,
        color=x,
        template="plotly_white",
    )

    fig.update_layout(
        title=title if title else None,
        showlegend=False,
        xaxis_title="County",
        yaxis_title="Registered Voters",
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

        color_continuous_scale=BLUES,

    )

    fig.update_traces(

        marker=dict(

            opacity=0.8,

            line=dict(

                color="white",

                width=0.5,

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
    Create an interactive line chart.
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

    return apply_theme(fig)


# =============================================================================
# TREEMAP
# =============================================================================

def treemap(
    df,
    path,
    values,
    title="Relative size of counties and constituencies",
    
):
    """
    Create a clean Plotly treemap.

    Parameters:
        df: DataFrame
        path: hierarchy columns e.g. ["County", "Constituency"]
        values: numeric column
        title: optional chart title
    """

    import plotly.express as px

    data = df.copy()

    # Clean hierarchy columns
    for col in path:
        data[col] = (
            data[col]
            .fillna("Total Registered Voters")
            .astype(str)
            .str.strip()
        )

    # Remove completely empty hierarchy rows
    for col in path:
        data = data[data[col] != ""]

    # Ensure values are numeric
    data[values] = (
        data[values]
        .astype(str)
        .str.replace(",", "")
    )

    data[values] = pd.to_numeric(
        data[values],
        errors="coerce"
    )

    # Remove invalid values
    data = data.dropna(subset=[values])

    if data.empty:
        return None

    fig = px.treemap(
        data,
        path=path,
        values=values
    )

    # Dashboard styling
    fig.update_layout(
        title=None,
        margin=dict(
            t=20,
            l=10,
            r=10,
            b=10
        )
    )

    fig.update_traces(
        textinfo="label+value",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Registered Voters: %{value:,}"
            "<extra></extra>"
        )
    )

    return fig
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

    fig.update_traces(

        hovertemplate=
        "<b>%{label}</b><br>"
        "Registered Voters: %{value:,.0f}"
        "<extra></extra>"

    )

    return apply_theme(fig)