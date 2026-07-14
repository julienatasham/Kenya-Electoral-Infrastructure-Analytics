"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE
    Metric Cards

DESCRIPTION
    Reusable Streamlit metric cards for displaying Key Performance
    Indicators (KPIs) throughout the KEIAP platform.

AUTHOR
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

import streamlit as st


# =============================================================================
# METRIC CARDS
# =============================================================================

def render_metric_cards(metrics: list[tuple[str, str]]) -> None:
    """
    Display KPI metric cards in a responsive row.

    Parameters
    ----------
    metrics : list[tuple[str, str]]

        Example
        -------
        [
            ("Registered Voters", "22,120,458"),
            ("Polling Stations", "46,229"),
            ("Constituencies", "290"),
            ("Counties", "47"),
        ]
    """

    if not metrics:

        st.warning("No metrics available.")

        return

    columns = st.columns(len(metrics))

    for column, (title, value) in zip(columns, metrics):

        with column:

            st.metric(

                label=title,

                value=value,

            )