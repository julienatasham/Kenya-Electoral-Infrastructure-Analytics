"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

PAGE
    Statistics

DESCRIPTION
    Provides an interactive statistical overview of Kenya's electoral
    infrastructure using Plotly visualizations and summary metrics.

AUTHOR
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import pandas as pd

from utils.loader import load_all_data
from utils.charts import (
    horizontal_bar_chart,
    donut_chart,
    histogram,
    box_plot,
    scatter_plot,
    treemap,
    sunburst_chart,
)

from scripts.metric_cards import render_metric_cards
# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="Statistics",
    page_icon="📊",
    layout="wide",
)

st.title("Statistics")

st.caption(
    """
    Explore Kenya's electoral infrastructure through interactive
    statistical analysis and visualizations.
    """
)
# =============================================================================
# LOAD DATA
# =============================================================================

polling_df, constituency_df, diaspora_df, prison_df = load_all_data()
# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

render_metric_cards(
    polling_df,
    constituency_df,
    diaspora_df,
    prison_df,
)
# =============================================================================
# FILTERS
# =============================================================================

st.divider()

left, right = st.columns(2)

counties = sorted(
    polling_df["county_name"].dropna().unique()
)

selected_county = left.selectbox(
    "County",
    ["All Counties"] + counties,
)

if selected_county == "All Counties":

    filtered_df = polling_df.copy()

else:

    filtered_df = polling_df[
        polling_df["county_name"] == selected_county
    ]

constituencies = sorted(
    filtered_df["constituency_name"].dropna().unique()
)

selected_constituency = right.selectbox(
    "Constituency",
    ["All Constituencies"] + constituencies,
)

if selected_constituency != "All Constituencies":

    filtered_df = filtered_df[
        filtered_df["constituency_name"]
        == selected_constituency
    ]
    # =============================================================================
# SUMMARY TABLES
# =============================================================================

county_summary = (

    filtered_df

    .groupby("county_name", as_index=False)

    ["registered_voters"]

    .sum()

    .sort_values(
        "registered_voters",
        ascending=False,
    )

)
# =============================================================================
# NATIONAL OVERVIEW
# =============================================================================

st.divider()

st.subheader("National Overview")

st.caption(
    """
    Compare the total number of registered voters across counties and
    examine each county's contribution to the national voter register.
    """
)

left_chart, right_chart = st.columns(2)
# =============================================================================
# REGISTERED VOTERS BY COUNTY
# =============================================================================

with left_chart:

    st.markdown("#### Registered Voters by County")

    st.caption(
        """
        Counties are ranked by the total number of registered voters.
        This visualization helps identify the largest electorates.
        """
    )

    fig = horizontal_bar_chart(

        county_summary,

        x="registered_voters",

        y="county_name",

        title="Registered Voters by County",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    if not county_summary.empty:

        top_county = county_summary.iloc[0]

        st.info(

            f"""
            **Insight**

            {top_county['county_name']} has the largest registered
            electorate with
            **{int(top_county['registered_voters']):,}**
            registered voters.
            """

        )
# =============================================================================
# COUNTY SHARE
# =============================================================================

with right_chart:

    st.markdown("#### County Share of Registered Voters")

    st.caption(
        """
        Shows each county's proportional contribution to the registered
        voter population.
        """
    )

    fig = donut_chart(

        county_summary,

        names="county_name",

        values="registered_voters",

        title="County Share",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    total = county_summary["registered_voters"].sum()

    top = county_summary.iloc[0]

    percentage = (

        top["registered_voters"]

        / total

        * 100

    )

    st.info(

        f"""
        **Insight**

        {top['county_name']} contributes approximately
        **{percentage:.1f}%**
        of the registered voters represented in the current view.
        """

    )
# =============================================================================
# STATISTICAL DISTRIBUTION
# =============================================================================

st.divider()

st.subheader("Statistical Distribution")

st.caption(
    """
    Explore how registered voters are distributed across polling
    stations and counties.
    """
)

left_chart, right_chart = st.columns(2)
with left_chart:

    st.markdown("#### Distribution of Registered Voters")

    st.caption(
        """
        Displays how polling stations are distributed according to
        their registered voter population.
        """
    )

    fig = histogram(

        filtered_df,

        column="registered_voters",

        title="Registered Voters Distribution",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.info(

        f"""
        **Insight**

        Average registered voters per polling station:

        **{filtered_df['registered_voters'].mean():,.0f}**
        """

    )
with right_chart:

    st.markdown("#### County Distribution")

    st.caption(
        """
        Compare the variation in registered voters across polling
        stations within each county.
        """
    )

    fig = box_plot(

        filtered_df,

        x="county_name",

        y="registered_voters",

        title="County Distribution",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.info(

        """
        **Insight**

        The box plot highlights the median, quartiles and outliers,
        making it easier to identify counties with unusually large
        polling stations.
        """
    )
