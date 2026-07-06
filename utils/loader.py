import os
import pandas as pd

# Project root
PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(PROJECT_DIR, "cleaned_csvs")


def load_polling_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "polling_station_clean.csv"),
        dtype=str
    )


def load_constituency_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "constituency_clean.csv"),
        dtype=str
    )


def load_diaspora_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "diaspora_clean.csv"),
        dtype=str
    )


def load_prison_data():
    return pd.read_csv(
        os.path.join(DATA_DIR, "prisons_clean.csv"),
        dtype=str
    )