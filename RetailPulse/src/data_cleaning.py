
from pathlib import Path
import pandas as pd
import numpy as np

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "Sample_Superstore.csv"
OUTPUT_DIR = BASE_DIR / "outputs"
CLEANED_PATH = OUTPUT_DIR / "cleaned_superstore.csv"


def clean_data():
    """Load, validate, and clean the retail transaction data."""

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH, encoding="cp1252")
    df.columns = df.columns.str.strip()

    required = [
        "Order Date", "Sales", "Profit",
        "Discount", "Category", "Sub-Category",
        "Region"
    ]

    missing = [col for col in required if col not in df.columns]

    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    original_rows = len(df)

    # Convert columns to correct data types
    df["Order Date"] = pd.to_datetime(
        df["Order Date"], errors="coerce"
    )

    for col in ["Sales", "Profit", "Discount"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Remove exact duplicate records
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()

    # Remove rows missing essential analytical fields
    df = df.dropna(subset=required).copy()

    # Add reusable analytical fields
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year

    df["Profit Margin"] = np.where(
        df["Sales"] != 0,
        df["Profit"] / df["Sales"],
        np.nan
    )

    df["Discount Band"] = np.select(
        [
            df["Discount"].eq(0),
            df["Discount"].gt(0) & df["Discount"].le(0.10),
            df["Discount"].gt(0.10) & df["Discount"].le(0.20),
            df["Discount"].gt(0.20) & df["Discount"].le(0.30),
            df["Discount"].gt(0.30)
        ],
        [
            "0% - No Discount",
            "1-10%",
            "11-20%",
            "21-30%",
            "Above 30%"
        ],
        default="Unknown"
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(CLEANED_PATH, index=False)

    print("DATA CLEANING COMPLETED")
    print("-" * 35)
    print(f"Original rows: {original_rows:,}")
    print(f"Exact duplicates removed: {duplicates:,}")
    print(f"Cleaned rows: {len(df):,}")
    print(f"Missing cells remaining: {int(df.isna().sum().sum()):,}")
    print(f"Sales: ${df['Sales'].sum():,.2f}")
    print(f"Profit: ${df['Profit'].sum():,.2f}")
    print(f"Output saved to: {CLEANED_PATH}")

    return df


if __name__ == "__main__":
    clean_data()
