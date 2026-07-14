"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

PAGE
    Statistics

DESCRIPTION
    Interactive statistical dashboard providing insights into
    Kenya's electoral infrastructure.

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

import utils.charts as charts

from utils.loader import load_all_data
from utils.theme import load_theme
from scripts.metric_cards import render_metric_cards

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(

    page_title="Statistics",

    page_icon="📊",

    layout="wide",

)

load_theme()

# =============================================================================
# LOAD DATA
# =============================================================================

polling_df, constituency_df, diaspora_df, prison_df = load_all_data()

# =============================================================================
# PAGE HEADER
# =============================================================================

st.title("📊 Electoral Statistics Dashboard")

st.caption(
    """
    Explore Kenya's electoral infrastructure through interactive
    statistical visualisations, descriptive analytics and electoral
    insights.
    """
)

st.divider()

# =============================================================================
# KEY PERFORMANCE INDICATORS
# =============================================================================

st.header("📌 National Electoral Snapshot")

st.markdown(
    """
    The indicators below summarise the current electoral register and
    provide an immediate overview of Kenya's electoral infrastructure.
    """
)
registered_voters = int(
    polling_df["registered_voters"].sum()
)

polling_stations = len(polling_df)

constituencies = constituency_df["constituency_name"].nunique()

counties = polling_df["county_name"].nunique()

average_station_size = round(
    polling_df["registered_voters"].mean()
)
metrics = [

    (
        "Registered Voters",
        f"{registered_voters:,}",
    ),

    (
        "Polling Stations",
        f"{polling_stations:,}",
    ),

    (
        "Constituencies",
        f"{constituencies:,}",
    ),

    (
        "Counties",
        f"{counties:,}",
    ),

    (
        "Average Polling Station Size",
        f"{average_station_size:,}",
    ),
    ]

render_metric_cards(metrics)

st.caption(
    """
    **Dashboard Summary**

    These key performance indicators provide a national overview of
    Kenya's electoral infrastructure. They form the foundation for the
    analyses presented throughout this dashboard.
    """
)
st.divider()
# =============================================================================
# FILTERS
# =============================================================================

st.header("🔎 Explore the Data")

st.markdown(
    """
    Filter the electoral register by **County** and **Constituency**.
    All visualisations and summaries below will automatically update
    based on your selection.
    """
)

left, right = st.columns(2)

# -------------------------------------------------------------------------
# County Filter
# -------------------------------------------------------------------------

counties = sorted(

    polling_df["county_name"]

    .dropna()

    .unique()

)

selected_county = left.selectbox(

    "Select County",

    ["All Counties"] + counties,

)

# -------------------------------------------------------------------------
# Apply County Filter
# -------------------------------------------------------------------------

if selected_county == "All Counties":

    filtered_df = polling_df.copy()

else:

    filtered_df = polling_df[

        polling_df["county_name"]

        == selected_county

    ]

# -------------------------------------------------------------------------
# Constituency Filter
# -------------------------------------------------------------------------

constituencies = sorted(

    filtered_df["constituency_name"]

    .dropna()

    .unique()

)

selected_constituency = right.selectbox(

    "Select Constituency",

    ["All Constituencies"] + constituencies,

)

# -------------------------------------------------------------------------
# Apply Constituency Filter
# -------------------------------------------------------------------------

if selected_constituency != "All Constituencies":

    filtered_df = filtered_df[

        filtered_df["constituency_name"]

        == selected_constituency

    ]

st.info(
    """
    💡 **How to use this dashboard**

    Select a county or constituency to focus your analysis.
    Every chart, table and summary below responds dynamically
    to your selections, allowing you to compare electoral
    registration patterns across different regions.
    """
)

st.divider()

# =============================================================================
# NATIONAL OVERVIEW
# =============================================================================

st.header("📊 National Overview")

st.markdown(
    """
    The visualisations below provide a national overview of voter
    registration across Kenya. They highlight where registered voters
    are concentrated and help identify counties that may require
    additional electoral resources during election planning.
    """
)

county_summary = (

    filtered_df

    .groupby(

        "county_name",

        as_index=False,

    )

    ["registered_voters"]

    .sum()

    .sort_values(

        "registered_voters",

        ascending=False,

    )

)


left, right = st.columns(2)

with left:

    st.subheader("Registered Voters by County")

    fig = charts.horizontal_bar_chart(

        county_summary,

        x="registered_voters",

        y="county_name",

        title="none",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        **Chart Caption**

        This chart compares the total number of registered voters
        across counties based on the selected filters.
        """
    )

    st.success(
        """
        💡 **Key Insight**

        Counties appearing at the top have the largest registered
        voter populations and therefore represent some of the most
        significant electoral regions in Kenya.
        """
    )
with right:

    st.subheader("County Share of Registered Voters")

    fig = charts.donut_chart(

        county_summary,

        names="county_name",

        values="registered_voters",

        title="none",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        **Chart Caption**

        Percentage contribution of each county to the national
        registered voter population.
        """
    )

    st.info(
        """
        📖 **Data Story**

        Kenya's registered voters are not distributed evenly across
        all counties. Counties with larger shares of registered voters
        require proportionally greater electoral planning, staffing,
        polling materials and logistical support.
        """
    )

st.divider()
# =============================================================================
# CONSTITUENCY ANALYSIS
# =============================================================================

st.header("🏛 Constituency Analysis")

st.markdown(
    """
    Constituencies form the core electoral units within counties.
    This section highlights constituencies with the largest registered
    voter populations while illustrating how they fit within the
    national electoral hierarchy.
    """
)

constituency_summary = (

    filtered_df

    .groupby(

        "constituency_name",

        as_index=False,

    )

    ["registered_voters"]

    .sum()

    .sort_values(

        "registered_voters",

        ascending=False,

    )

)

left, right = st.columns(2)

with left:

    st.subheader("Top Constituencies")

    fig = charts.vertical_bar_chart(

        constituency_summary.head(15),

        x="constituency_name",

        y="registered_voters",

        title="Top Constituencies",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        **Chart Caption**

        Constituencies ranked by total registered voters.
        """
    )

    st.success(
        """
        💡 **Key Insight**

        Constituencies with larger electorates generally require
        additional polling stations, election officials and voting
        materials to ensure efficient election management.
        """
    )
    
with right:

    st.subheader("Electoral Hierarchy")

    fig = charts.treemap (
        constituency_df,
        path=["county_name", "constituency_name"],
        values="registered_voters"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.caption(
        """
        **Chart Caption**

        Hierarchical representation of counties and constituencies
        based on registered voters.
        """
    )

    st.info(
        """
        📖 **Data Story**

        Larger blocks represent constituencies with more registered
        voters. The treemap quickly highlights where electoral
        activity is concentrated within each county.
        """
    )

st.divider()

# =============================================================================
# STATISTICAL ANALYSIS
# =============================================================================

st.header("📈 Statistical Analysis")

st.markdown(
    """
    Statistical visualisations help reveal how registered voters are
    distributed across polling stations. They make it easier to identify
    patterns, variations and unusually large polling stations that may
    require additional election planning.
    """
)

left, right = st.columns(2)

with left:

    st.subheader("Distribution of Registered Voters")

    fig = charts.histogram(

        filtered_df,

        column="registered_voters",

        title="",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        **Chart Caption**

        Frequency distribution of registered voters across polling stations.
        """
    )

    st.success(
        """
        💡 **Key Insight**

        Most polling stations fall within a similar registration range,
        while a smaller number have significantly larger electorates.

        This helps identify stations that may require additional electoral
        resources on polling day.
        """
    )
    
with right:

    st.subheader("Variation Across Counties")

    fig = charts.box_plot(

        filtered_df,

        x="county_name",

        y="registered_voters",

        title="none",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        **Chart Caption**

        Comparison of voter registration across counties.
        """
    )

    st.info(
        """
        📖 **Data Story**

        The box plot summarises how voter registration varies within each
        county. Counties with wider spreads contain polling stations with
        very different registration sizes, while isolated points indicate
        unusually large or unusually small polling stations.
        """
    )

st.divider()
st.subheader("📊 Statistical Summary")

summary_col1, summary_col2, summary_col3 = st.columns(3)

summary_col1.metric(
    "Average Polling Station Size",
    f"{filtered_df['registered_voters'].mean():.0f}"
)

summary_col2.metric(
    "Median",
    f"{filtered_df['registered_voters'].median():.0f}"
)

summary_col3.metric(
    "Maximum",
    f"{filtered_df['registered_voters'].max():.0f}"
)

# =============================================================================
# ELECTORAL HIERARCHY
# =============================================================================

st.divider()

st.header("🌳 Electoral Hierarchy")

st.markdown(
    """
    The charts below show how registered voters are distributed across
    Kenya's electoral hierarchy. The treemap highlights the relative
    size of counties and constituencies, while the line chart ranks the
    largest constituencies by registered voters.
    """
)

# -------------------------------------------------------------------------
# Aggregate data to avoid duplicate hierarchy errors
# -------------------------------------------------------------------------

treemap_df = (

    filtered_df

    .groupby(

        [

            "county_name",

            "constituency_name",

        ],

        as_index=False,

    )["registered_voters"]

    .sum()

)

largest_constituencies = (

    treemap_df

    .sort_values(

        "registered_voters",

        ascending=False,

    )

    .head(15)

)

left, right = st.columns(2)

with left:

    fig = charts.treemap(

        treemap_df,

        path=[

            "county_name",

            "constituency_name",

        ],

        values="registered_voters",

        title="County → Constituency Hierarchy",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Treemap showing the relative size of constituencies within
        each county.
        """
    )

with right:

    fig = charts.horizontal_bar_chart(

        largest_constituencies,

        x="registered_voters",

        y="constituency_name",

        title="Top 15 Constituencies",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Constituencies with the largest registered voter populations.
        """
    )

st.info(
    """
📖 **Data Story**

Voter registration is not evenly distributed across Kenya.
A relatively small number of constituencies account for a
large proportion of registered voters, indicating where
electoral resources may need additional reinforcement.
"""
)
# =============================================================================
# TOP CONSTITUENCIES BY REGISTERED VOTERS
# =============================================================================

st.divider()

st.header("🏆 Top Constituencies by Registered Voters")

top_constituencies = (
    filtered_df
    .sort_values(
        "registered_voters",
        ascending=False,
    )
    .head(20)
)

fig = charts.horizontal_bar_chart(
    top_constituencies,
    x="registered_voters",
    y="constituency_name",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.caption(
    """
    Constituencies with the highest registered voter populations.
    """
)

st.success(
    """
🗳️ **Electoral Insight**

Constituencies with larger voter populations typically require
greater electoral resources, including polling officials,
KIEMS kits, ballot papers, logistics support and enhanced
election-day coordination.
"""
)

# =============================================================================
# EXPLORE DATASET
# =============================================================================

st.divider()

st.header("🔍 Explore the Dataset")

search = st.text_input(
    "Search Electoral Records",
    placeholder="County or Constituency...",
)

if search:

    dataset = filtered_df[
        filtered_df.astype(str)
        .apply(
            lambda column: column.str.contains(
                search,
                case=False,
                na=False,
            )
        )
        .any(axis=1)
    ]

else:

    dataset = filtered_df.copy()

st.caption(f"Showing **{len(dataset):,}** records.")

st.dataframe(
    dataset,
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    "⬇ Download Filtered Dataset",
    dataset.to_csv(index=False),
    "keiap_statistics.csv",
    "text/csv",
)

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

st.divider()

st.header("📌 Executive Summary")

total_voters = int(filtered_df["registered_voters"].sum())

total_constituencies = filtered_df["constituency_name"].nunique()

total_counties = filtered_df["county_name"].nunique()

largest_county = (
    filtered_df
    .groupby("county_name")["registered_voters"]
    .sum()
    .idxmax()
)

largest_constituency = (
    filtered_df
    .sort_values("registered_voters", ascending=False)
    .iloc[0]["constituency_name"]
)

summary1, summary2 = st.columns(2)

with summary1:

    st.metric(
        "Registered Voters",
        f"{total_voters:,}",
    )

    st.metric(
        "Constituencies",
        f"{total_constituencies:,}",
    )

with summary2:

    st.metric(
        "Counties",
        f"{total_counties:,}",
    )

    st.metric(
        "Largest Constituency",
        largest_constituency,
    )

st.markdown(
    f"""
### Summary

This analysis covers **{total_counties} counties** and
**{total_constituencies} constituencies**, representing
**{total_voters:,} registered voters**.

### Key Findings

- **{largest_county}** has the largest registered voter population.

- **{largest_constituency}** is the largest constituency by registered voters.

- Voter registration is concentrated within a relatively small number of counties and constituencies.

- Areas with high voter populations require proportionally greater electoral resources, staffing and operational planning.
"""
)

st.success(
    """
🗳️ **Planning Insight**

The Statistics Dashboard provides evidence-based insights that support
electoral planning, voter distribution analysis, resource allocation
and operational preparedness across Kenya.
"""
)