"""
Dataset Download Script
Fetches the PhiUSIIL Phishing URL (Website) Dataset from the UCI Machine Learning Repository (ID 967)
and saves it to data/raw/phiusiil.csv.
"""

import os
import sys
import pandas as pd


def download_phiusiil_dataset():
    output_dir = os.path.join("data", "raw")
    output_file = os.path.join(output_dir, "phiusiil.csv")
    os.makedirs(output_dir, exist_ok=True)

    print("=" * 60)
    print("PhiUSIIL Phishing URL Dataset Downloader")
    print("Source: UCI Machine Learning Repository (ID: 967)")
    print("=" * 60)

    try:
        from ucimlrepo import fetch_ucirepo
    except ImportError:
        print("[ERROR] 'ucimlrepo' package is not installed.")
        print("Please install it using: pip install ucimlrepo")
        sys.exit(1)

    print("Fetching dataset from UCI repository (ID 967)... This may take a minute.")
    try:
        dataset = fetch_ucirepo(id=967)
    except Exception as e:
        print(f"[ERROR] Failed to fetch dataset: {e}")
        print("Tip: Check your internet connection or download manually from:")
        print("https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset")
        sys.exit(1)

    X = dataset.data.features
    y = dataset.data.targets

    print("\nDataset successfully fetched!")
    print(f"Features shape : {X.shape}")
    print(f"Targets shape  : {y.shape}")

    print("\nFeature sample columns:")
    print(X.columns.tolist()[:10], "... (total", len(X.columns), "columns)")

    print("\nTarget column names:")
    print(y.columns.tolist())

    # Combine features and targets into a single dataframe
    df = pd.concat([X, y], axis=1)

    # Save to disk
    df.to_csv(output_file, index=False)
    print(f"\n[SUCCESS] Dataset saved to: {output_file}")
    print(f"Final shape: {df.shape}")


if __name__ == "__main__":
    download_phiusiil_dataset()
