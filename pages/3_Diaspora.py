"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

PAGE:
    Diaspora Voter Registration

DESCRIPTION:
    Interactive dashboard for analysing Kenya's diaspora voter
    registration by country and registration centre.

AUTHOR:
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
diaspora_df = diaspora_df[
    diaspora_df["county_code"].astype(str).str.upper() != "TOTAL"
]
# =============================================================================
# CLEAN DATA
# =============================================================================

diaspora_df = diaspora_df.copy()

diaspora_df.columns = (
    diaspora_df.columns
    .str.strip()
    .str.lower()
)

text_columns = [
    "county_name",
    "country_name",
    "registration_centre_name",
    "polling_station_name",
]

for column in text_columns:

    if column in diaspora_df.columns:

        diaspora_df[column] = (
            diaspora_df[column]
            .astype(str)
            .str.strip()
        )

diaspora_df["registered_voters"] = pd.to_numeric(
    diaspora_df["registered_voters"],
    errors="coerce",
)

diaspora_df = diaspora_df.dropna(
    subset=["registered_voters"]
)

# =============================================================================
# HEADER
# =============================================================================

st.title("Diaspora Voter Registration")

st.caption(
    """
    Explore Kenya's diaspora voter registration across countries,
    registration centres and polling stations.
    """
)

st.divider()

# =============================================================================
# KEY PERFORMANCE INDICATORS
# =============================================================================

total_voters = int(
    diaspora_df["registered_voters"].sum()
)

countries = (
    diaspora_df["country_name"]
    .nunique()
)

centres = (
    diaspora_df["registration_centre_name"]
    .nunique()
)

polling_stations = (
    diaspora_df["polling_station_name"]
    .nunique()
)

metrics = [

    (
        "Registered Voters",
        f"{total_voters:,}",
    ),

    (
        "Countries",
        f"{countries:,}",
    ),

    (
        "Registration Centres",
        f"{centres:,}",
    ),

    (
        "Polling Stations",
        f"{polling_stations:,}",
    ),

]

from scripts.metric_cards import render_metric_cards

render_metric_cards(metrics)

st.divider()

# =============================================================================
# COUNTRY FILTER
# =============================================================================

country_list = sorted(
    diaspora_df["country_name"]
    .dropna()
    .unique()
)

selected_country = st.selectbox(
    "Select Country",
    ["All Countries"] + country_list,
)

if selected_country == "All Countries":

    filtered_df = diaspora_df.copy()

else:

    filtered_df = diaspora_df[
        diaspora_df["country_name"] == selected_country
    ]
    
st.write(filtered_df["registered_voters"].dtype)
st.divider()

# =============================================================================
# COUNTRY OVERVIEW
# =============================================================================

country_summary = (

    filtered_df

    .groupby(
        "country_name",
        as_index=False,
    )["registered_voters"]

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

        title="",

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        """
        Total registered diaspora voters by country.
        """
    )

with right:

    st.subheader("Country Share")

    fig = charts.donut_chart(

        country_summary,

        names="country_name",

        values="registered_voters",

        title="",

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        """
        Percentage contribution of each country to the
        diaspora voter register.
        """
    )

st.divider()

# =============================================================================
# REGISTRATION CENTRES
# =============================================================================

centre_summary = (

    filtered_df

    .groupby(
        "registration_centre_name",
        as_index=False,
    )["registered_voters"]

    .sum()

    .sort_values(
        "registered_voters",
        ascending=False,
    )

)

left, right = st.columns(2)

with left:

    st.subheader("Top Registration Centres")

    fig = charts.vertical_bar_chart(

        centre_summary.head(15),

        x="registration_centre_name",

        y="registered_voters",

        title="",

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        """
        Registration centres with the highest numbers of
        registered diaspora voters.
        """
    )

with right:

    st.subheader("Registration Hierarchy")

    hierarchy_df = (

        filtered_df

        .groupby(
            [
                "country_name",
                "registration_centre_name",
            ],
            as_index=False,
        )["registered_voters"]

        .sum()

    )

    fig = charts.treemap(

        hierarchy_df,

        path=[
            "country_name",
            "registration_centre_name",
        ],

        values="registered_voters",

        title="",

    )

    st.plotly_chart(
        fig,
        use_container_width=True,
    )

    st.caption(
        """
        Hierarchical view of registered voters from
        country level down to registration centres.
        """
    )

st.divider()

# =============================================================================
# TOP REGISTRATION CENTRES TABLE
# =============================================================================

st.subheader("Top 15 Registration Centres")

top_centres = (

    filtered_df

    .groupby(
        [
            "country_name",
            "registration_centre_name",
        ],
        as_index=False,
    )["registered_voters"]

    .sum()

    .sort_values(
        "registered_voters",
        ascending=False,
    )

    .head(15)

)

st.dataframe(

    top_centres,

    use_container_width=True,

    hide_index=True,

)

st.caption(
    """
    Registration centres ranked by total registered
    diaspora voters.
    """
)

st.divider()

# =============================================================================
# DATASET EXPLORER
# =============================================================================

st.subheader("Dataset Explorer")

search = st.text_input(
    "Search",
    placeholder="Search country or registration centre..."
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

st.divider()

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

# =============================================================================
# EXECUTIVE SUMMARY
# =============================================================================

largest_country = (
    country_summary.iloc[0]["country_name"]
)

largest_centre = (
    top_centres.iloc[0]["registration_centre_name"]
)

st.subheader("Executive Summary")

st.markdown(
    f"""
This dashboard summarises **{total_voters:,}** registered diaspora voters
across **{countries} countries**, **{centres} registration centres** and
**{polling_stations} polling stations**.

### Key Findings

- **{largest_country}** has the largest registered diaspora voter population.
- **{largest_centre}** is the largest registration centre.
- Diaspora voter registration is concentrated within a relatively small
  number of registration centres.
- The dashboard supports planning for staffing, election materials,
  logistics and voter outreach outside Kenya.
"""
)

st.divider()

st.caption(
    """
    Kenya Electoral Infrastructure Analytics Platform (KEIAP)

    Diaspora Voter Registration Dashboard
    """
)