"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Metric Cards

PURPOSE:
    Provides reusable metric cards for displaying key performance
    indicators throughout the platform.

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

import streamlit as st

# =============================================================================
# KPI ROW
# =============================================================================

def render_metric_cards(metrics: list[tuple[str, str]]) -> None:
    """
    Render a responsive row of Streamlit metric cards.

    Parameters
    ----------
    metrics : list of tuple
        Each tuple should contain:

            (
                metric_title,
                metric_value
            )

    Example
    -------
    metrics = [

        ("Registered Voters", "22.1M"),

        ("Counties", "47"),

        ("Polling Stations", "46,229")

    ]
    """

    columns = st.columns(len(metrics))

    for column, (title, value) in zip(columns, metrics):

        with column:

            st.metric(

                label=title,

                value=value,
            )