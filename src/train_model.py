"""
XGBoost Model Training Script
Trains an XGBoost Binary Classifier on preprocessed URL features.
Saves model and feature columns to models/.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import argparse
import joblib
import pandas as pd
from xgboost import XGBClassifier
from src.preprocessing import preprocess_data


def train_xgboost(use_gpu=False, n_estimators=150, max_depth=7, learning_rate=0.05):
    print("=" * 60)
    print("XGBoost Fraudulent Website Classifier Training")
    print(f"Target Hardware : {'NVIDIA GPU (CUDA)' if use_gpu else 'CPU'}")
    print("=" * 60)

    # 1. Load preprocessed train and test data
    X_train, X_test, y_train, y_test = preprocess_data()

    # 2. Configure model hyperparameters
    params = {
        "n_estimators": n_estimators,
        "max_depth": max_depth,
        "learning_rate": learning_rate,
        "subsample": 0.8,
        "colsample_bytree": 0.8,
        "objective": "binary:logistic",
        "eval_metric": "logloss",
        "tree_method": "hist",
        "random_state": 42,
    }

    if use_gpu:
        print("[INFO] Configuring XGBoost for NVIDIA CUDA acceleration...")
        params["device"] = "cuda"
    else:
        params["n_jobs"] = -1

    model = XGBClassifier(**params)

    # 3. Train model with timing
    print(f"\nTraining on {len(X_train):,} samples with {X_train.shape[1]} features...")
    start_time = time.time()
    model.fit(X_train, y_train)
    training_time = time.time() - start_time

    print(f"\n[SUCCESS] Training Completed in: {training_time:.2f} seconds")

    # 4. Save model artifacts
    os.makedirs("models", exist_ok=True)
    model_path = os.path.join("models", "xgboost_fraud_detector.pkl")
    features_path = os.path.join("models", "feature_columns.pkl")

    joblib.dump(model, model_path)
    joblib.dump(list(X_train.columns), features_path)

    print(f"Model saved to: {model_path}")
    print(f"Feature columns saved to: {features_path}")

    return model, training_time, (X_train, X_test, y_train, y_test)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train XGBoost Model for Phishing Detection")
    parser.add_argument("--gpu", action="store_true", help="Enable NVIDIA GPU acceleration via CUDA")
    parser.add_argument("--estimators", type=int, default=150, help="Number of gradient boosted trees")
    parser.add_argument("--depth", type=int, default=7, help="Maximum tree depth")
    parser.add_argument("--lr", type=float, default=0.05, help="Learning rate")

    args = parser.parse_args()
    train_xgboost(
        use_gpu=args.gpu,
        n_estimators=args.estimators,
        max_depth=args.depth,
        learning_rate=args.lr
    )
