"""
===============================================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM (KEIAP)

MODULE:
    Data Loader

PURPOSE:
    Provides centralized functions for loading all cleaned electoral datasets.
    Cleans extracted PDF artefacts before datasets are used across the platform.

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
# INTERNAL CSV LOADER
# =============================================================================


def _load_csv(filename: str) -> pd.DataFrame:
    """
    Load a CSV file from the cleaned datasets directory.

    Parameters
    ----------
    filename : str
        Dataset filename.

    Returns
    -------
    pandas.DataFrame
        Loaded dataframe.
    """

    filepath = DATA_FOLDER / filename

    if not filepath.exists():
        st.error(f"Dataset not found:\n{filepath}")
        st.stop()

    return pd.read_csv(filepath)


# =============================================================================
# DATA CLEANING FUNCTIONS
# =============================================================================


def _clean_polling_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove extraction artefacts from polling station dataset.

    Removes:
    - accidental CSV header row loaded as data
    - TOTAL summary row
    - missing geographical records
    """

    df = df.copy()

    # Remove accidental header row:
    # county_name = 1, constituency_name = 3
    df = df[
        ~df["county_name"]
        .astype(str)
        .str.match(r"^\d+$", na=False)
    ]

    # Remove TOTAL summary row
    df = df[
        df["county_name"].notna()
    ]

    # Remove records without constituency information
    df = df[
        df["constituency_name"].notna()
    ]

    # Standardise text columns
    text_columns = [
        "county_name",
        "constituency_name",
        "ward_name",
        "registration_centre_name",
        "polling_station_name",
    ]

    for column in text_columns:
        if column in df.columns:
            df[column] = (
                df[column]
                .astype(str)
                .str.strip()
                .str.upper()
            )

    return df.reset_index(drop=True)


# =============================================================================
# INDIVIDUAL DATASETS
# =============================================================================


@st.cache_data
def load_polling_data() -> pd.DataFrame:
    """
    Load and clean polling station dataset.
    """

    df = _load_csv(
        "polling_station_clean.csv"
    )

    return _clean_polling_data(df)


@st.cache_data
def load_constituency_data() -> pd.DataFrame:
    """
    Load constituency dataset.
    """

    return _load_csv(
        "constituency_clean.csv"
    )


@st.cache_data
def load_diaspora_data() -> pd.DataFrame:
    """
    Load diaspora voter dataset.
    """

    return _load_csv(
        "diaspora_clean.csv"
    )


@st.cache_data
def load_prison_data() -> pd.DataFrame:
    """
    Load prison voter dataset.
    """

    return _load_csv(
        "prisons_clean.csv"
    )


# =============================================================================
# LOAD ALL DATASETS
# =============================================================================


@st.cache_data
def load_all_data():
    """
    Load all datasets used by KEIAP.

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