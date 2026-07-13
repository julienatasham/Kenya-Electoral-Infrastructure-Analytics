"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Data Loader

PURPOSE:
    Provides centralized functions for loading all cleaned electoral datasets.
    Keeping dataset paths in one place simplifies maintenance and ensures
    consistency throughout the application.

AUTHOR:
    Julie Natasha
===============================================================================
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

# =============================================================================
# PROJECT DIRECTORIES
# =============================================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_FOLDER = PROJECT_ROOT / "cleaned_csvs"

# =============================================================================
# INTERNAL LOADER
# =============================================================================


def _load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the cleaned datasets directory.

    Parameters
    ----------
    filename : str
        Name of the CSV file.

    Returns
    -------
    pandas.DataFrame
        Loaded dataset.
    """

    filepath = DATA_FOLDER / filename

    if not filepath.exists():
        st.error(f"Dataset not found:\n{filepath}")
        st.stop()

    return pd.read_csv(filepath)


# =============================================================================
# INDIVIDUAL DATASETS
# =============================================================================

@st.cache_data
def load_polling_data() -> pd.DataFrame:
    """Load polling station dataset."""
    return _load_csv("polling_station_clean.csv")


@st.cache_data
def load_constituency_data() -> pd.DataFrame:
    """Load constituency dataset."""
    return _load_csv("constituency_clean.csv")


@st.cache_data
def load_diaspora_data() -> pd.DataFrame:
    """Load diaspora dataset."""
    return _load_csv("diaspora_clean.csv")


@st.cache_data
def load_prison_data() -> pd.DataFrame:
    """Load prison voter dataset."""
    return _load_csv("prisons_clean.csv")


# =============================================================================
# LOAD ALL DATASETS
# =============================================================================

@st.cache_data
def load_all_data():
    """
    Load every dataset used by the platform.

    Returns
    -------
    tuple
        (
            polling_df,
            constituency_df,
            diaspora_df,
            prison_df
        )
    """

    return (
        load_polling_data(),
        load_constituency_data(),
        load_diaspora_data(),
        load_prison_data(),
    )