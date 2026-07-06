import os
import re
import pandas as pd
import pdfplumber

# ==================================================
# PATHS
# ==================================================

PROJECT_DIR = r"C:\Users\USER\OneDrive\Desktop\projects\Voter Registration Analytics"

RAW_DIR = os.path.join(PROJECT_DIR, "raw_pdfs")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "output_csvs")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================================================
# CLEAN CELL
# ==================================================

def clean_cell(value):
    if value is None:
        return ""

    value = str(value)

    value = value.replace("\n", " ")
    value = re.sub(r"\s+", " ", value)

    return value.strip()


# ==================================================
# EXTRACT TABLES
# ==================================================

def extract_tables(pdf):

    rows = []

    for page in pdf.pages:

        tables = page.extract_tables()

        if not tables:
            continue

        for table in tables:

            for row in table:

                if row is None:
                    continue

                cleaned = [clean_cell(cell) for cell in row]

                if any(cleaned):
                    rows.append(cleaned)

    return rows


# ==================================================
# FALLBACK TEXT EXTRACTION
# ==================================================

def extract_text(pdf):

    rows = []

    for page in pdf.pages:

        text = page.extract_text()

        if not text:
            continue

        for line in text.split("\n"):

            line = clean_cell(line)

            if line:
                rows.append([line])

    return rows


# ==================================================
# PROCESS ONE PDF
# ==================================================

def process_pdf(pdf_path):

    print(f"\nProcessing: {os.path.basename(pdf_path)}")

    with pdfplumber.open(pdf_path) as pdf:

        rows = extract_tables(pdf)

        if rows:

            print(f"  ✔ Extracted {len(rows)} table rows")

        else:

            print("  ⚠ No tables found. Falling back to text extraction...")

            rows = extract_text(pdf)

            print(f"  ✔ Extracted {len(rows)} text rows")

    return rows


# ==================================================
# SAVE CSV
# ==================================================

def save_csv(rows, pdf_name):

    if not rows:
        print("  ✖ Nothing extracted")
        return

    max_cols = max(len(r) for r in rows)

    padded = []

    for row in rows:
        padded.append(row + [""] * (max_cols - len(row)))

    df = pd.DataFrame(padded)

    output_name = os.path.splitext(pdf_name)[0] + ".csv"

    output_path = os.path.join(OUTPUT_DIR, output_name)

    df.to_csv(
        output_path,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"  ✔ Saved → {output_name}")


# ==================================================
# MAIN
# ==================================================

def main():

    pdfs = [f for f in os.listdir(RAW_DIR) if f.lower().endswith(".pdf")]

    if not pdfs:
        print("No PDFs found.")
        return

    print(f"Found {len(pdfs)} PDFs\n")

    for pdf_file in pdfs:

        pdf_path = os.path.join(RAW_DIR, pdf_file)

        try:

            rows = process_pdf(pdf_path)

            save_csv(rows, pdf_file)

        except Exception as e:

            print(f"✖ Failed: {pdf_file}")
            print(e)

    print("\nFinished.")


# ==================================================

if __name__ == "__main__":
    main()