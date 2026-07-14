"""
=========================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM

PAGE:
    Prison Voters Analytics

Purpose:
    Explore registered voters in prison voting centres.
=========================================================
"""


import streamlit as st
import pandas as pd

from utils.loader import load_prison_data


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Prison Voters Analytics",
    page_icon="🔒",
    layout="wide"
)


# =========================================================
# HEADER
# =========================================================

st.title("🔒 Prison Voters Analytics")

st.write(
    """
    This module provides analysis of registered voters
    within prison voting centres across Kenya.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    prisons = load_prison_data()

except Exception as e:

    st.error(
        f"Unable to load prison dataset: {e}"
    )

    st.stop()



# =========================================================
# CLEAN DATA TYPES
# =========================================================

prisons["registered_voters"] = pd.to_numeric(
    prisons["registered_voters"],
    errors="coerce"
)


# =========================================================
# SUMMARY CARDS
# =========================================================

total_voters = int(
    prisons["registered_voters"].sum()
)


total_centres = prisons[
    "registration_centre_name"
].nunique()


total_stations = prisons[
    "polling_station_name"
].nunique()



col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Total Prison Voters",
        f"{total_voters:,}"
    )


with col2:

    st.metric(
        "Registration Centres",
        total_centres
    )


with col3:

    st.metric(
        "Polling Stations",
        total_stations
    )



st.divider()



# =========================================================
# SEARCH
# =========================================================

st.subheader("🔎 Search Prison Voting Centre")


search = st.text_input(
    "Search prison facility",
    placeholder=
    "Example: Shimo La Tewa..."
)



if search:

    results = prisons[
        prisons.astype(str)
        .apply(
            lambda row:
            row.str.contains(
                search,
                case=False,
                na=False
            ).any(),
            axis=1
        )
    ]


    st.success(
        f"{len(results)} result(s) found"
    )


    st.dataframe(
        results,
        use_container_width=True
    )



else:

    st.dataframe(
        prisons,
        use_container_width=True,
        height=400
    )



# =========================================================
# ANALYTICS
# =========================================================

st.divider()


left, right = st.columns(2)



with left:

    st.subheader(
        "Top Prison Voting Centres"
    )


    top_prisons = (
        prisons.groupby(
            "polling_station_name"
        )["registered_voters"]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )


    st.bar_chart(
        top_prisons
    )



with right:

    st.subheader(
        "Voters by County"
    )


    county_summary = (
        prisons.groupby(
            "county_name"
        )["registered_voters"]
        .sum()
        .sort_values(
            ascending=False
        )
    )


    st.bar_chart(
        county_summary
    )



# =========================================================
# DOWNLOAD
# =========================================================

st.divider()

st.subheader(
    "📥 Export Data"
)


csv = prisons.to_csv(
    index=False
)


st.download_button(
    label="Download Prison Voter Data",
    data=csv,
    file_name="prison_voters_analysis.csv",
    mime="text/csv"
)