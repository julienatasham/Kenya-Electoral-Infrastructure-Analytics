"""
====================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    search_engine.py

PURPOSE:
    This module provides reusable search functions for the
    Polling Centre Finder application.

The search engine allows users to search the official IEBC
polling station dataset using:

    • Polling Station Name
    • Registration Centre
    • Ward
    • Constituency
    • County
    • Polling Station Code

AUTHOR:
    Julie Natasha
====================================================================
"""

# ====================================================================
# IMPORT REQUIRED LIBRARIES
# ====================================================================

import os
import pandas as pd

# ====================================================================
# PROJECT PATHS
# ====================================================================

# Root project folder
PROJECT_DIR = r"C:\Users\USER\OneDrive\Desktop\projects\Kenya Electoral Infrastructure Analytics"

# Path to the cleaned polling station dataset
DATA_FILE = os.path.join(
    PROJECT_DIR,
    "cleaned_csvs",
    "polling_station_clean.csv"
)

# ====================================================================
# LOAD DATASET
# ====================================================================

# Read the cleaned polling station CSV.
# dtype=str ensures codes with leading zeros are preserved.
df = pd.read_csv(DATA_FILE, dtype=str)

print(f"Loaded {len(df):,} polling stations.")

# ====================================================================
# POLLING STATION SEARCH CLASS
# ====================================================================

class PollingStationSearch:
    """
    Provides different search methods for the polling
    station dataset.

    Every search method returns a filtered pandas DataFrame.
    """

    def __init__(self, dataframe):
        """
        Initialize the search engine.

        Parameters
        ----------
        dataframe : pandas.DataFrame
            Clean polling station dataset.
        """
        self.df = dataframe

    # ===============================================================
    # SEARCH BY POLLING STATION NAME
    # ===============================================================

    def by_polling_station(self, name):
        """
        Search polling stations by name.
        """

        return self.df[
            self.df["polling_station_name"]
            .str.contains(name, case=False, na=False)
        ]

    # ===============================================================
    # SEARCH BY REGISTRATION CENTRE
    # ===============================================================

    def by_registration_centre(self, centre):
        """
        Search registration centres.
        """

        return self.df[
            self.df["registration_centre_name"]
            .str.contains(centre, case=False, na=False)
        ]

    # ===============================================================
    # SEARCH BY COUNTY
    # ===============================================================

    def by_county(self, county):
        """
        Search by county name.
        """

        return self.df[
            self.df["county_name"]
            .str.contains(county, case=False, na=False)
        ]

    # ===============================================================
    # SEARCH BY CONSTITUENCY
    # ===============================================================

    def by_constituency(self, constituency):
        """
        Search by constituency.
        """

        return self.df[
            self.df["constituency_name"]
            .str.contains(constituency, case=False, na=False)
        ]

    # ===============================================================
    # SEARCH BY WARD
    # ===============================================================

    def by_ward(self, ward):
        """
        Search by ward.
        """

        return self.df[
            self.df["ward_name"]
            .str.contains(ward, case=False, na=False)
        ]

    # ===============================================================
    # SEARCH BY POLLING STATION CODE
    # ===============================================================

    def by_code(self, code):
        """
        Search using the unique polling station code.
        """

        return self.df[
            self.df["polling_station_code"] == code
        ]

# ====================================================================
# CREATE SEARCH ENGINE OBJECT
# ====================================================================

search = PollingStationSearch(df)

# ====================================================================
# TESTING
# ====================================================================

# This block only runs when this file is executed directly.
# It will NOT run when imported into the Streamlit application.

if __name__ == "__main__":

    print("\nTesting Search Engine...\n")

    print(search.by_county("MOMBASA"))

    print(search.by_polling_station("BOMU"))