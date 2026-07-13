
"""
=========================================================
KENYA ELECTORAL INFRASTRUCTURE ANALYTICS PLATFORM

Script:
    clean_datasets.py

Purpose:
    Automatically clean extracted IEBC CSV datasets.

Datasets Supported:
    - Constituency
    - Polling Station
    - Diaspora
    - Prison Voters

Output:
    cleaned_csvs/
=========================================================
"""

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
# STANDARD DATASET SCHEMAS
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
    ]

}



# =========================================================
# DATASET IDENTIFICATION
# =========================================================

def detect_dataset(filename):

    filename = filename.lower()

    if "constituency" in filename:
        return "constituency"

    if "polling" in filename:
        return "polling"

    if "diaspora" in filename:
        return "diaspora"

    if "prison" in filename:
        return "prisons"

    return None



# =========================================================
# REMOVE UNWANTED ROWS
# =========================================================

def remove_titles(df):

    first = df.iloc[:,0].astype(str)

    return df[
        ~first.str.contains(
            "REGISTERED VOTERS|REGISTER OF VOTERS",
            case=False,
            na=False
        )
    ]



def remove_headers(df):

    first = df.iloc[:,0].astype(str)

    return df[
        ~first.str.contains(
            "County Code|Code|Country Code",
            case=False,
            na=False
        )
    ]



def remove_blank_rows(df):

    return df.dropna(how="all")



# =========================================================
# STANDARDIZE COLUMNS
# =========================================================

def rename_columns(df, dataset):

    schema = SCHEMAS[dataset]

    if len(df.columns) >= len(schema):

        df = df.iloc[:, :len(schema)]

        df.columns = schema

    else:

        print(
            "Warning: Column count does not match schema"
        )

    return df



# =========================================================
# CLEAN TEXT
# =========================================================

def clean_text(df):

    for col in df.columns:

        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.replace(
                r"\s+",
                " ",
                regex=True
            )
        )

    return df



# =========================================================
# CONVERT VOTER NUMBERS
# =========================================================

def convert_voters(df):

    if "registered_voters" in df.columns:

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
# VALIDATION
# =========================================================

def validate(df):

    print(f"Rows: {len(df):,}")

    print(
        f"Duplicates: {df.duplicated().sum():,}"
    )

    print("\nColumns:")
    print(list(df.columns))

    print("\nMissing Values:")
    print(df.isna().sum())



# =========================================================
# CLEAN SINGLE FILE
# =========================================================

def clean_dataset(filepath):

    filename = os.path.basename(filepath)

    dataset = detect_dataset(filename)


    if dataset is None:

        print(
            f"Skipping {filename}"
        )

        return



    print("\n" + "="*60)
    print(
        f"CLEANING {filename}"
    )
    print("="*60)



    df = pd.read_csv(
        filepath,
        header=None,
        dtype=str,
        keep_default_na=False
    )


    print(
        f"Original rows: {len(df):,}"
    )


    df = remove_blank_rows(df)

    df = remove_titles(df)

    df = remove_headers(df)

    df = rename_columns(
        df,
        dataset
    )

    df = clean_text(df)

    df = df.drop_duplicates()

    df = convert_voters(df)



    validate(df)



    output = os.path.join(
        OUTPUT_DIR,
        filename.replace(
            ".csv",
            "_clean.csv"
        )
    )


    df.to_csv(
        output,
        index=False
    )


    print(
        f"\nSaved: {output}"
    )



# =========================================================
# RUN ALL DATASETS
# =========================================================

def main():

    files = [
        f
        for f in os.listdir(RAW_DIR)
        if f.lower().endswith(".csv")
    ]


    print(
        f"\nFound {len(files)} CSV file(s)"
    )


    for file in files:

        clean_dataset(
            os.path.join(
                RAW_DIR,
                file
            )
        )


    print("\nCleaning completed successfully.")



if __name__ == "__main__":
    main()
