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
# Statistics page excludes non-geographical records
statistics_df = polling_df[
    polling_df["county_name"].notna()
    & polling_df["constituency_name"].notna()
    & ~polling_df["county_name"].astype(str).str.match(r"^\d+$")
    & ~polling_df["constituency_name"].astype(str).str.match(r"^\d+$")
    & ~polling_df["county_name"].isin(
        ["DIASPORA", "PRISONS"]
    )
].copy()


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

# Statistics page excludes Diaspora and Prison records
# Statistics page excludes non-geographical records
statistics_df = polling_df[
    polling_df["county_name"].notna()
    & polling_df["constituency_name"].notna()
    & ~polling_df["county_name"].astype(str).str.match(r"^\d+$")
    & ~polling_df["constituency_name"].astype(str).str.match(r"^\d+$")
    & ~polling_df["county_name"].isin(
        ["DIASPORA", "PRISONS"]
    )
].copy()

registered_voters = int(
    statistics_df["registered_voters"].sum()
)

polling_stations = len(statistics_df)

constituencies = (
    statistics_df["constituency_name"]
    .nunique()
)

counties = (
    statistics_df["county_name"]
    .nunique()
)

average_station_size = round(
    statistics_df["registered_voters"].mean()
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
# =============================================================================#
st.divider()

st.subheader("📊 Polling Station Size Analysis")

st.write(
    """
    This section analyses the distribution of registered voters across Kenya's
    polling stations. It provides a general overview of polling station capacity
    and supports understanding of electoral infrastructure requirements.
    """
)

# Clean data for analysis
size_df = filtered_df.copy()

size_df = size_df[
    size_df["registered_voters"].notna()
]

size_df = size_df[
    size_df["polling_station_name"].notna()
]


largest_voters = size_df["registered_voters"].max()

largest_station = (
    size_df[
        size_df["registered_voters"] == largest_voters
    ]
    .iloc[0]
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Largest Polling Station Capacity",
        f"{int(largest_voters):,} voters"
    )

with col2:
    st.metric(
        "Average Polling Station Size",
        f"{int(size_df['registered_voters'].mean()):,} voters"
    )

with col3:
    st.metric(
        "Total Polling Stations",
        f"{len(size_df):,}"
    )



st.divider()

# =============================================================================
# DISTRIBUTION OF POLLING STATION SIZES
# =============================================================================

left, right = st.columns([2,1])

with left:

    st.subheader("Distribution of Registered Voters per Polling Station")

    fig = charts.histogram(
        filtered_df,
        column="registered_voters",
        title="",
    )

    fig.update_traces(
        xbins=dict(
            start=0,
            end=1000,
            size=100,
        )
    )

    fig.update_layout(
        xaxis_title="Registered Voters",
        yaxis_title="Number of Polling Stations",
    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

with right:

    st.subheader("Summary Statistics")

    st.metric(
        "Average",
        f"{filtered_df['registered_voters'].mean():.0f}",
    )

    st.metric(
        "Median",
        f"{filtered_df['registered_voters'].median():.0f}",
    )

    st.metric(
        "Minimum",
        f"{filtered_df['registered_voters'].min():.0f}",
    )

    st.metric(
        "Maximum",
        f"{filtered_df['registered_voters'].max():.0f}",
    )

st.caption(
    """
The histogram groups all polling stations into 100-voter intervals,
illustrating how registered voters are distributed across Kenya's
polling stations.
"""
)

st.success(
    """
📈 **Statistical Insight**

Most polling stations are concentrated within the middle voter ranges,
while comparatively few stations accommodate exceptionally large
electorates. Understanding this distribution helps election managers
plan staffing, election materials, KIEMS deployment and polling day
operations more effectively.
"""
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
# LARGEST CONSTITUENCIES
# =============================================================================

st.divider()

st.header("🏆 Largest Constituencies")

largest_constituencies = (
    filtered_df
    .groupby(
        "constituency_name",
        as_index=False,
    )["registered_voters"]
    .sum()
    .sort_values(
        "registered_voters",
        ascending=False,
    )
    .head(20)
)

fig = charts.horizontal_bar_chart(
    df=largest_constituencies,
    x="registered_voters",
    y="constituency_name",
    title="",
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

st.caption(
    """
    This chart ranks the 20 constituencies with the highest number of
    registered voters based on the current filters.
    """
)

st.info(
    """
    **Electoral Insight**

    Constituencies with larger registered voter populations generally
    require more polling stations, election officials, KIEMS kits,
    ballot papers and logistical support to ensure efficient election
    management.
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
# EXECUTIVE SUMMARY DATA
# =============================================================================

summary_df = (
    filtered_df
    .groupby(
        ["county_name", "constituency_name"],
        as_index=False,
    )["registered_voters"]
    .sum()
)

total_voters = int(summary_df["registered_voters"].sum())

total_constituencies = (
    summary_df["constituency_name"]
    .nunique()
)

total_counties = (
    summary_df["county_name"]
    .nunique()
)

largest_county = (
    summary_df
    .groupby("county_name")["registered_voters"]
    .sum()
    .idxmax()
)

largest_constituency = (
    summary_df
    .sort_values(
        "registered_voters",
        ascending=False,
    )
    .iloc[0]["constituency_name"]
)

st.markdown(
    f"""
### Summary

This analysis covers **{total_counties} counties**two being "prisons" and "diaspora" and
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