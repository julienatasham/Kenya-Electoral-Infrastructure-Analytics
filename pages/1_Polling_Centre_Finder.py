"""
=====================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Polling Centre Finder

PURPOSE:
    Search the official IEBC polling station dataset.

SUPPORTED SEARCHES:
    • Polling Station Name
    • Registration Centre
    • Ward
    • Constituency
    • County
    • Polling Station Code

AUTHOR:
    Julie Natasha

=====================================================================
"""


# =====================================================================
# IMPORTS
# =====================================================================

import streamlit as st

from utils.loader import load_all_data

from scripts.search_engine import PollingStationSearch



# =====================================================================
# PAGE CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title="Polling Centre Finder",
    page_icon="📍",
    layout="wide",
)



# =====================================================================
# LOAD DATA
# =====================================================================

polling_df, constituency_df, diaspora_df, prison_df = load_all_data()


# Use only polling station data for this page

df = polling_df



# =====================================================================
# INITIALIZE SEARCH ENGINE
# =====================================================================

search = PollingStationSearch(df)



# =====================================================================
# HEADER
# =====================================================================

st.title("📍 Polling Centre Finder")


st.markdown(
    """
Search the official IEBC polling station register.

You can search by:

- Polling Station
- Registration Centre
- Ward
- Constituency
- County
- Polling Station Code
"""
)



# =====================================================================
# SEARCH OPTIONS
# =====================================================================

search_by = st.selectbox(
    "Search By",
    [
        "Polling Station",
        "Registration Centre",
        "Ward",
        "Constituency",
        "County",
        "Polling Station Code",
    ],
)



# =====================================================================
# SEARCH INPUT
# =====================================================================

query = st.text_input(
    "Enter your search"
)



# =====================================================================
# EXECUTE SEARCH
# =====================================================================

results = None


if query:

    if search_by == "Polling Station":

        results = search.by_polling_station(query)


    elif search_by == "Registration Centre":

        results = search.by_registration_centre(query)


    elif search_by == "Ward":

        results = search.by_ward(query)


    elif search_by == "Constituency":

        results = search.by_constituency(query)


    elif search_by == "County":

        results = search.by_county(query)


    elif search_by == "Polling Station Code":

        results = search.by_code(query)



# =====================================================================
# DISPLAY RESULTS
# =====================================================================

if results is not None:

    st.subheader("Search Results")

    st.write(
        f"Records Found: **{len(results):,}**"
    )


    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True,
    )


else:

    st.info(
        "Enter a search term to begin."
    )



# =====================================================================
# DOWNLOAD RESULTS
# =====================================================================

if results is not None and not results.empty:

    csv = (
        results
        .to_csv(index=False)
        .encode("utf-8")
    )


    st.download_button(
        label="Download Results (CSV)",
        data=csv,
        file_name="polling_station_search_results.csv",
        mime="text/csv",
    )