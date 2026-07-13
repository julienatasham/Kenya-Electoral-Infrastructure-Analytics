"""
=====================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Polling Centre Finder

PURPOSE:
    This page allows users to search the official IEBC polling
    station database using different search criteria.

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
from utils.loader import load_polling_data
from scripts.search_engine import PollingStationSearch

# =====================================================================
# PAGE CONFIGURATION
# =====================================================================

st.set_page_config(
    page_title="Polling Centre Finder",
    page_icon="📍",
    layout="wide"
)

# =====================================================================
# LOAD DATA
# =====================================================================
# Load the cleaned polling station dataset.
# The loader keeps all file paths in one location, making the project
# easier to maintain.

df = load_polling_data()

# =====================================================================
# INITIALIZE SEARCH ENGINE
# =====================================================================
# Create an instance of the search engine using the loaded dataset.

search = PollingStationSearch(df)

# =====================================================================
# PAGE HEADER
# =====================================================================

st.title("📍 Polling Centre Finder")

st.markdown("""
Search the official IEBC polling station register.

Use the options below to search by:

- Polling Station
- Registration Centre
- Ward
- Constituency
- County
- Polling Station Code
""")

# =====================================================================
# SEARCH OPTIONS
# =====================================================================

search_by = st.selectbox(
    "Search By",
    (
        "Polling Station",
        "Registration Centre",
        "Ward",
        "Constituency",
        "County",
        "Polling Station Code"
    )
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

    st.write(f"Records Found: **{len(results):,}**")

    st.dataframe(
        results,
        use_container_width=True,
        hide_index=True
    )

else:

    st.info(
        "Enter a search term to begin."
    )

# =====================================================================
# DOWNLOAD RESULTS
# =====================================================================

if results is not None and not results.empty:

    csv = results.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Results (CSV)",
        data=csv,
        file_name="polling_station_search_results.csv",
        mime="text/csv"
    )