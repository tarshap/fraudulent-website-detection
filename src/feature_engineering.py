"""
Feature Engineering and Alignment Pipeline
Ensures consistency between training features and real-time inference inputs.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.url_features import extract_url_features


def build_features_from_url(url: str, feature_columns: list = None) -> pd.DataFrame:
    """
    Extracts features from a URL and aligns the columns with the model's expected schema.
    Missing features are filled with 0, and extra features are dropped.
    """
    raw_features = extract_url_features(url)
    df = pd.DataFrame([raw_features])

    if feature_columns is not None:
        # Align with expected feature columns
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[feature_columns]

    return df


def align_features(df: pd.DataFrame, expected_columns: list) -> pd.DataFrame:
    """
    Ensures that input DataFrame matches the exact column order expected by the model.
    """
    for col in expected_columns:
        if col not in df.columns:
            df[col] = 0
    return df[expected_columns]


if __name__ == "__main__":
    test_url = "https://secure-banking-login.update-alert.com/auth"
    feats = build_features_from_url(test_url)
    print("Engineered URL Features:")
    print(feats.T)
