"""
Data Preprocessing and Train/Test Split Module
Extracts URL-level characteristics from dataset URLs and splits into
stratified 80/20 training and testing sets.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from sklearn.model_selection import train_test_split
from src.url_features import extract_url_features, URL_FEATURE_COLUMNS


def preprocess_data(file_path="data/raw/phiusiil.csv", sample_size=None, test_size=0.20, random_state=42):
    """
    Extracts features for URLs in the dataset and returns stratified train/test splits.
    """
    processed_train_path = os.path.join("data", "processed", "train.csv")
    processed_test_path = os.path.join("data", "processed", "test.csv")

    if os.path.exists(processed_train_path) and os.path.exists(processed_test_path) and sample_size is None:
        print(f"Loading cached preprocessed datasets from data/processed/...")
        train_df = pd.read_csv(processed_train_path)
        test_df = pd.read_csv(processed_test_path)

        y_train = train_df["label"]
        X_train = train_df.drop(columns=["label"])
        y_test = test_df["label"]
        X_test = test_df.drop(columns=["label"])

        print(f"Loaded train: {X_train.shape[0]:,} samples | test: {X_test.shape[0]:,} samples")
        return X_train, X_test, y_train, y_test

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}. Run 'python src/download_dataset.py' first.")

    print(f"Loading raw dataset from: {file_path}")
    df = pd.read_csv(file_path)
    print(f"Dataset shape: {df.shape}")

    if sample_size and sample_size < len(df):
        print(f"Sampling {sample_size:,} records for fast experimentation...")
        df = df.sample(n=sample_size, random_state=random_state).reset_index(drop=True)

    print("Extracting URL features across dataset...")
    feature_rows = [extract_url_features(url) for url in df["URL"]]
    X = pd.DataFrame(feature_rows)
    y = df["label"]

    print(f"Extracted {X.shape[1]} features across {len(X):,} URLs.")

    # Stratified split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y
    )

    print(f"Train set: {X_train.shape[0]:,} samples | Test set: {X_test.shape[0]:,} samples")

    # Cache preprocessed splits
    os.makedirs(os.path.join("data", "processed"), exist_ok=True)
    pd.concat([X_train, y_train], axis=1).to_csv(processed_train_path, index=False)
    pd.concat([X_test, y_test], axis=1).to_csv(processed_test_path, index=False)
    print(f"Cached processed splits to data/processed/")

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    X_train, X_test, y_train, y_test = preprocess_data(sample_size=60000)
