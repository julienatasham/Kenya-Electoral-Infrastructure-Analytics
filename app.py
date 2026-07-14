"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Home Dashboard

PURPOSE:
    Executive dashboard providing a national overview of Kenya's
    electoral infrastructure.

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st

from scripts.sidebar import render_sidebar

from utils.theme import load_theme
from utils.loader import load_all_data
from utils.formatting import (
    format_compact,
    format_number,
)
from utils.charts import (
    bar_chart,
    pie_chart,
)

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(

    page_title="KEIAP",

    layout="wide",

    initial_sidebar_state="expanded",

)

# =============================================================================
# LOAD GLOBAL THEME
# =============================================================================

load_theme()

# =============================================================================
# SIDEBAR
# =============================================================================

render_sidebar()

# =============================================================================
# LOAD DATA
# =============================================================================

polling_df, constituency_df, diaspora_df, prison_df = load_all_data()

# =============================================================================
# DASHBOARD HEADER
# =============================================================================

st.title("Kenya Electoral Infrastructure Analytics Platform")

st.caption(
    "National Electoral Infrastructure Dashboard"
)

st.divider()

# =============================================================================
# KEY PERFORMANCE INDICATORS
# =============================================================================

registered_voters = int(
    polling_df["registered_voters"].sum()
)

polling_stations = len(polling_df)

constituencies = polling_df["constituency_name"].nunique()

counties = polling_df["county_name"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(

        "Registered Voters",

        format_compact(registered_voters),

        help=format_number(registered_voters),

    )

with col2:

    st.metric(

        "Polling Stations",

        format_number(polling_stations),

    )

with col3:

    st.metric(

        "Constituencies",

        constituencies,

    )

with col4:

    st.metric(

        "Counties",

        counties,

    )

st.divider()

# =============================================================================
# VISUALIZATIONS
# =============================================================================

left, right = st.columns(2)

# -------------------------------------------------------------------------
# Registered Voters by County
# -------------------------------------------------------------------------

county_summary = (

    polling_df

    .groupby("county_name", as_index=False)

    ["registered_voters"]

    .sum()

    .sort_values(

        "registered_voters",

        ascending=False,

    )

)

with left:

    st.subheader("Registered Voters by County")

    fig = bar_chart(

        county_summary.head(10),

        x="county_name",

        y="registered_voters",

        title="Top 10 Counties",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

# -------------------------------------------------------------------------
# County Share
# -------------------------------------------------------------------------

with right:

    st.subheader("County Share of Registered Voters")

    fig = pie_chart(

        county_summary.head(10),

        names="county_name",

        values="registered_voters",

        title="Top 10 Counties",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

# =============================================================================
# DATASET SUMMARY
# =============================================================================

st.divider()

st.subheader("Dataset Summary")

summary = {

    "Polling Stations": len(polling_df),

    "Constituencies": len(constituency_df),

    "Diaspora Stations": len(diaspora_df),

    "Prison Stations": len(prison_df),

}

st.dataframe(

    summary,

    use_container_width=True,

)