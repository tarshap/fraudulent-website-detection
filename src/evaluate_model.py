"""
Model Evaluation and PPT Visual Evidence Generation
Evaluates the trained XGBoost model and saves confusion matrix, ROC curve,
feature importance charts, and metrics CSV.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay
)
from src.preprocessing import preprocess_data


def evaluate_model(model_path="models/xgboost_fraud_detector.pkl", features_path="models/feature_columns.pkl"):
    print("=" * 60)
    print("Evaluating XGBoost Fraudulent Website Classifier")
    print("=" * 60)

    if not (os.path.exists(model_path) and os.path.exists(features_path)):
        raise FileNotFoundError(f"Model or feature artifacts missing. Train model first with 'python src/train_model.py'.")

    model = joblib.load(model_path)
    feature_columns = joblib.load(features_path)

    _, X_test, _, y_test = preprocess_data()

    print(f"Running evaluation on {len(X_test):,} test samples...")

    preds = model.predict(X_test)
    probs = model.predict_proba(X_test)[:, 1]

    # Metrics
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)
    auc = roc_auc_score(y_test, probs)

    print("\n" + "-" * 35)
    print(f"Accuracy  : {acc:.4f} ({acc*100:.2f}%)")
    print(f"Precision : {prec:.4f}")
    print(f"Recall    : {rec:.4f}")
    print(f"F1-Score  : {f1:.4f}")
    print(f"ROC-AUC   : {auc:.4f}")
    print("-" * 35)

    print("\nDetailed Classification Report:")
    print(classification_report(y_test, preds, target_names=["Phishing (0)", "Legitimate (1)"]))

    # Output directories
    os.makedirs(os.path.join("results", "figures"), exist_ok=True)
    os.makedirs(os.path.join("results", "metrics"), exist_ok=True)

    # 1. Confusion Matrix Chart
    print("\nGenerating Confusion Matrix...")
    fig, ax = plt.subplots(figsize=(6, 5))
    ConfusionMatrixDisplay.from_predictions(
        y_test,
        preds,
        display_labels=["Phishing", "Legitimate"],
        cmap="Blues",
        ax=ax
    )
    plt.title("XGBoost Fraudulent Website Detection - Confusion Matrix")
    cm_path = os.path.join("results", "figures", "confusion_matrix.png")
    plt.tight_layout()
    plt.savefig(cm_path, dpi=300)
    plt.close()
    print(f"Saved: {cm_path}")

    # 2. ROC Curve Chart
    print("Generating ROC Curve...")
    fig, ax = plt.subplots(figsize=(6, 5))
    RocCurveDisplay.from_predictions(y_test, probs, name="XGBoost", ax=ax)
    plt.plot([0, 1], [0, 1], "k--", label="Chance (AUC = 0.50)")
    plt.title("XGBoost ROC Curve - Phishing Detection")
    plt.legend(loc="lower right")
    roc_path = os.path.join("results", "figures", "roc_curve.png")
    plt.tight_layout()
    plt.savefig(roc_path, dpi=300)
    plt.close()
    print(f"Saved: {roc_path}")

    # 3. Feature Importance Chart
    print("Generating Feature Importance...")
    importance = pd.Series(model.feature_importances_, index=feature_columns).sort_values(ascending=False)
    top_n = min(len(feature_columns), 20)
    top_features = importance.head(top_n).sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, max(6, top_n * 0.35)))
    top_features.plot(kind="barh", color="#1e40af", ax=ax)
    plt.title(f"Top {top_n} URL Features Used by XGBoost")
    plt.xlabel("Importance Score")
    fi_path = os.path.join("results", "figures", "feature_importance.png")
    plt.tight_layout()
    plt.savefig(fi_path, dpi=300)
    plt.close()
    print(f"Saved: {fi_path}")

    # 4. Save Metrics CSV
    metrics_data = {
        "Metric": ["Accuracy", "Precision", "Recall", "F1-Score", "ROC-AUC"],
        "Score": [acc, prec, rec, f1, auc]
    }
    metrics_df = pd.DataFrame(metrics_data)
    metrics_path = os.path.join("results", "metrics", "model_comparison.csv")
    metrics_df.to_csv(metrics_path, index=False)
    print(f"Saved: {metrics_path}")

    print("\n[SUCCESS] Evaluation and visual artifacts generation complete!")


if __name__ == "__main__":
    try:
        evaluate_model()
    except Exception as e:
        print(f"[ERROR] Evaluation failed: {e}")
