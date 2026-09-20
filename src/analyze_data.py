"""
Dataset Inspection and Exploratory Analysis Script
Inspects schema, datatypes, missing values, duplicates, and class balance of data/raw/phiusiil.csv.
"""

import os
import sys
import pandas as pd


def analyze_dataset(file_path="data/raw/phiusiil.csv"):
    print("=" * 60)
    print(f"Inspecting Dataset: {file_path}")
    print("=" * 60)

    if not os.path.exists(file_path):
        print(f"[ERROR] Dataset file not found at: {file_path}")
        print("Please run: python src/download_dataset.py first.")
        sys.exit(1)

    df = pd.read_csv(file_path)

    print(f"\n1. Dimensions: {df.shape[0]:,} rows, {df.shape[1]} columns")

    print("\n2. Columns:")
    for idx, col in enumerate(df.columns, 1):
        print(f"  {idx:2d}. {col} ({df[col].dtype})")

    print("\n3. Missing Values:")
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]
    if len(missing_cols) == 0:
        print("  No missing values found across all columns.")
    else:
        print(missing_cols)

    duplicates = df.duplicated().sum()
    print(f"\n4. Duplicate Rows: {duplicates:,} ({duplicates / len(df) * 100:.2f}%)")

    # Determine likely target column
    candidate_targets = [c for c in df.columns if c.lower() in ["label", "target", "class", "phishing", "result"]]
    if candidate_targets:
        target_col = candidate_targets[0]
        print(f"\n5. Target Column Distribution ('{target_col}'):")
        print(df[target_col].value_counts(dropna=False))
        print("\nTarget Percentage:")
        print(df[target_col].value_counts(normalize=True) * 100)
    else:
        print("\n5. Target column not automatically identified. Please inspect column list.")

    print("\n[DONE] Inspection completed.")


if __name__ == "__main__":
    analyze_dataset()
