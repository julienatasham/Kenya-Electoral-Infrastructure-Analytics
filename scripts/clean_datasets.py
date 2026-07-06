"""
=========================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM

Script: clean_datasets.py

Purpose:
    Clean every extracted IEBC CSV automatically.

Datasets Supported:
    - Constituency
    - Polling Station
    - Diaspora
    - Prison

Output:
    Clean CSVs saved in cleaned_csvs/
=========================================================
"""

# =========================================================
# IMPORTS
# =========================================================

import os
import pandas as pd

# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_DIR = r"C:\Users\USER\OneDrive\Desktop\projects\Kenya Electoral Infrastructure Analytics"

RAW_DIR = os.path.join(PROJECT_DIR, "raw_csvs")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "cleaned_csvs")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# STANDARD SCHEMAS
# =========================================================

SCHEMAS = {

    "constituency": [
        "county_code",
        "county_name",
        "constituency_code",
        "constituency_name",
        "registered_voters"
    ],

    "polling": [
        "county_code",
        "county_name",
        "constituency_code",
        "constituency_name",
        "ward_code",
        "ward_name",
        "registration_centre_code",
        "registration_centre_name",
        "polling_station_code",
        "polling_station_name",
        "registered_voters"
    ],

    "diaspora": [
        "country_code",
        "country_name",
        "registration_area_code",
        "registration_area_name",
        "registration_centre_name",
        "registration_centre_code",
        "polling_station_code",
        "polling_station_name",
        "registered_voters"
    ],

    "prisons": [
        # Update this once we inspect the prison dataset
    ]

}

# =========================================================
# DATASET DETECTION
# =========================================================

def detect_dataset(filename):

    filename = filename.lower()

    if "constituency" in filename:
        return "constituency"

    elif "polling" in filename:
        return "polling"

    elif "diaspora" in filename:
        return "diaspora"

    elif "prison" in filename:
        return "prisons"

    return None


# =========================================================
# REMOVE REPORT TITLES
# =========================================================

def remove_titles(df):

    first_col = df.iloc[:, 0].astype(str)

    titles = (
        first_col.str.contains(
            "REGISTERED VOTERS",
            case=False,
            na=False
        )
        |
        first_col.str.contains(
            "REGISTER OF VOTERS",
            case=False,
            na=False
        )
    )

    return df[~titles]


# =========================================================
# REMOVE REPEATED HEADERS
# =========================================================

def remove_headers(df):

    first_col = df.iloc[:, 0].astype(str)

    repeated = (
        first_col.str.contains(
            "County Code",
            case=False,
            na=False
        )
        |
        first_col.str.contains(
            "^Code$",
            case=False,
            na=False
        )
    )

    return df[~repeated]


# =========================================================
# REMOVE INDEX ROWS
# =========================================================

def remove_index_rows(df):

    first_col = df.iloc[:, 0].astype(str)

    return df[first_col != "0"]


# =========================================================
# STANDARDIZE COLUMNS
# =========================================================

def rename_columns(df, dataset):

    schema = SCHEMAS.get(dataset)

    if not schema:
        return df

    if len(df.columns) >= len(schema):

        df = df.iloc[:, :len(schema)]

        df.columns = schema

    return df


# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(df):

    for column in df.columns:

        df[column] = (
            df[column]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return df


# =========================================================
# CONVERT REGISTERED VOTERS
# =========================================================

def convert_voters(df):

    if "registered_voters" not in df.columns:
        return df

    df["registered_voters"] = (
        df["registered_voters"]
        .str.replace(",", "", regex=False)
    )

    df["registered_voters"] = pd.to_numeric(
        df["registered_voters"],
        errors="coerce"
    )

    return df


# =========================================================
# VALIDATE DATA
# =========================================================

def validate(df):

    print(f"Rows: {len(df):,}")

    print(f"Duplicates: {df.duplicated().sum():,}")

    print("\nMissing Values")

    print(df.isna().sum())


# =========================================================
# CLEAN ONE DATASET
# =========================================================

def clean_dataset(filepath):

    filename = os.path.basename(filepath)

    dataset = detect_dataset(filename)

    if dataset is None:

        print(f"Skipping {filename}")

        return

    print("=" * 60)
    print(f"Cleaning: {filename}")
    print("=" * 60)

    df = pd.read_csv(
        filepath,
        dtype=str,
        keep_default_na=False
    )

    print(f"Original rows: {len(df):,}")

    df = df.dropna(how="all")

    df = remove_titles(df)

    df = remove_headers(df)

    df = remove_index_rows(df)

    df = rename_columns(df, dataset)

    df = clean_text(df)

    df = df.drop_duplicates()

    df = convert_voters(df)

    validate(df)

    output = os.path.join(
        OUTPUT_DIR,
        filename.replace(".csv", "_clean.csv")
    )

    df.to_csv(
        output,
        index=False
    )

    print(f"\nSaved: {output}\n")


# =========================================================
# MAIN
# =========================================================

def main():

    csv_files = [
        file
        for file in os.listdir(RAW_DIR)
        if file.lower().endswith(".csv")
    ]

    print(f"\nFound {len(csv_files)} CSV file(s).\n")

    for file in csv_files:

        clean_dataset(
            os.path.join(RAW_DIR, file)
        )

    print("=" * 60)
    print("Cleaning completed successfully.")
    print("=" * 60)


if __name__ == "__main__":
    main()