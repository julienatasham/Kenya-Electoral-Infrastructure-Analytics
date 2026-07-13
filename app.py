"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE
    Home Dashboard

DESCRIPTION
    Executive dashboard providing a national overview of Kenya's
    electoral infrastructure.
===============================================================================
"""


import streamlit as st


from config import (
    APP_NAME,
    PAGE_TITLE,
)


from utils.theme import load_theme

from utils.loader import load_all_data

from utils.charts import (
    registered_voters_by_county,
    county_distribution,
    polling_stations_per_county,
)


from scripts.sidebar import render_sidebar

from scripts.page_header import render_page_header

from scripts.metric_cards import metric_row



# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title=PAGE_TITLE,
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
# HEADER
# =============================================================================

render_page_header(
    title="National Electoral Infrastructure Dashboard",
    description=(
        "Interactive analytical platform for exploring Kenya's "
        "electoral infrastructure datasets."
    ),
)



# =============================================================================
# KEY METRICS
# =============================================================================

total_counties = (
    constituency_df["county_name"]
    .nunique()
)


total_constituencies = (
    constituency_df["constituency_name"]
    .nunique()
)


total_polling_stations = (
    polling_df["polling_station_name"]
    .nunique()
)


total_registered_voters = int(
    constituency_df["registered_voters"]
    .sum()
)



metric_row(
    [
        {
            "label": "Counties",
            "value": total_counties,
        },

        {
            "label": "Constituencies",
            "value": total_constituencies,
        },

        {
            "label": "Polling Stations",
            "value": total_polling_stations,
        },

        {
            "label": "Registered Voters",
            "value": f"{total_registered_voters:,}",
        },
    ]
)



# =============================================================================
# DASHBOARD CHARTS
# =============================================================================

st.divider()


st.subheader("Electoral Infrastructure Overview")


chart1, chart2 = st.columns(2)


with chart1:

    st.plotly_chart(
        registered_voters_by_county(constituency_df),
        use_container_width=True,
    )


with chart2:

    st.plotly_chart(
        county_distribution(constituency_df),
        use_container_width=True,
    )



st.divider()


st.subheader("Polling Infrastructure")


st.plotly_chart(
    polling_stations_per_county(polling_df),
    use_container_width=True,
)