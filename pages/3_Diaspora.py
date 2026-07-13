
"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

PAGE
    Diaspora Voter Registration

DESCRIPTION
    Interactive dashboard providing insights into Kenya's
    diaspora voter registration statistics.

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

from utils.loader import load_diaspora_data
from utils.theme import load_theme
from scripts.metric_cards import render_metric_cards

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(

    page_title="Diaspora Voters",

    page_icon="🌍",

    layout="wide",

)

load_theme()

# =============================================================================
# LOAD DATA
# =============================================================================

diaspora_df = load_diaspora_data()

# =============================================================================
# HEADER
# =============================================================================

st.title("Diaspora Voter Registration")

st.caption(
    """
    Explore Kenya's diaspora voter registration statistics
    by country, registration area and registration centre.
    """
)

st.divider()
# =============================================================================
# KEY PERFORMANCE INDICATORS
# =============================================================================

total_voters = int(diaspora_df["registered_voters"].sum())

countries = diaspora_df["country_name"].nunique()

areas = diaspora_df["registration_area_name"].nunique()

centres = diaspora_df["registration_centre_name"].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Registered Voters",
    f"{total_voters:,}",
)

c2.metric(
    "Countries",
    countries,
)

c3.metric(
    "Registration Areas",
    areas,
)

c4.metric(
    "Registration Centres",
    centres,
)

st.divider()
# =============================================================================
# COUNTRY FILTER
# =============================================================================

countries = sorted(
    diaspora_df["country_name"]
    .dropna()
    .unique()
)

selected_country = st.selectbox(

    "Select Country",

    ["All Countries"] + countries,

)

if selected_country == "All Countries":

    filtered_df = diaspora_df.copy()

else:

    filtered_df = diaspora_df[
        diaspora_df["country_name"] == selected_country
    ]

st.divider()
# =============================================================================
# COUNTRY OVERVIEW
# =============================================================================

country_summary = (

    filtered_df

    .groupby(
        "country_name",
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

    st.subheader("Registered Voters by Country")

    fig = charts.horizontal_bar_chart(

        country_summary,

        x="registered_voters",

        y="country_name",

        title="Registered Voters",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Registered diaspora voters by country.
        Countries with the highest registered voter populations
        appear at the top.
        """
    )
with right:

    st.subheader("Country Share")

    fig = charts.donut_chart(

        country_summary,

        names="country_name",

        values="registered_voters",

        title="Diaspora Share",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Percentage contribution of each country to the
        total diaspora voter register.
        """
    )

st.divider()

# =============================================================================
# REGISTRATION AREAS
# =============================================================================

area_summary = (

    filtered_df

    .groupby(
        "registration_area_name",
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

    st.subheader("Registration Areas")

    fig = charts.vertical_bar_chart(

        area_summary,

        x="registration_area_name",

        y="registered_voters",

        title="Registration Areas",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Registered voters aggregated by diaspora
        registration area.
        """
    )
with right:

    st.subheader("Registration Hierarchy")

    fig = charts.treemap(

        filtered_df,

        path=[
            "country_name",
            "registration_area_name",
            "registration_centre_name",
        ],

        values="registered_voters",

        title="Registration Centres",

    )

    st.plotly_chart(

        fig,

        use_container_width=True,

    )

    st.caption(
        """
        Hierarchical view of diaspora registration
        centres and their registered voter totals.
        """
    )

st.divider()
# =============================================================================
# REGISTRATION HIERARCHY
# =============================================================================

st.subheader("Registration Hierarchy")

fig = charts.sunburst_chart(

    filtered_df,

    path=[
        "country_name",
        "registration_area_name",
        "registration_centre_name",
    ],

    values="registered_voters",

    title="Diaspora Registration Hierarchy",

)

st.plotly_chart(

    fig,

    use_container_width=True,

)

st.caption(
    """
    Drill down from country to registration area and finally to
    individual registration centres based on registered voters.
    """
)

st.divider()
# =============================================================================
# TOP REGISTRATION CENTRES
# =============================================================================

st.subheader("Top Registration Centres")

top_centres = (

    filtered_df

    .sort_values(
        "registered_voters",
        ascending=False,
    )

    [[
        "country_name",
        "registration_area_name",
        "registration_centre_name",
        "registered_voters",
    ]]

    .head(15)

)

st.dataframe(

    top_centres,

    use_container_width=True,

    hide_index=True,

)

st.caption(
    """
    The fifteen registration centres with the highest number of
    registered diaspora voters.
    """
)

st.divider()
# =============================================================================
# DATASET
# =============================================================================

st.subheader("Diaspora Dataset")

search = st.text_input(
    "Search",
    placeholder="Type a country, registration area or centre..."
)

display_df = filtered_df.copy()

if search:

    display_df = display_df[

        display_df.astype(str)

        .apply(

            lambda row:

            row.str.contains(
                search,
                case=False,
                na=False,
            )

        )

        .any(axis=1)

    ]

st.dataframe(

    display_df,

    use_container_width=True,

    hide_index=True,

)
# =============================================================================
# DOWNLOAD
# =============================================================================

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(

    label="📥 Download Filtered Dataset",

    data=csv,

    file_name="diaspora_statistics.csv",

    mime="text/csv",

)
st.divider()

st.caption(
    """
    Kenya Electoral Infrastructure Analytics Platform (KEIAP)

    Diaspora Voter Registration Dashboard
    """
)
    