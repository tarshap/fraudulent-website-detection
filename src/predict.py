"""
Inference Module for Real-Time Fraudulent Website Prediction
Extracts URL features, aligns with model schema, and returns class prediction and risk score.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
import joblib
import pandas as pd
from src.url_features import extract_url_features
from src.feature_engineering import build_features_from_url


class PhishingPredictor:
    def __init__(self, model_path="models/xgboost_fraud_detector.pkl", features_path="models/feature_columns.pkl"):
        self.model = None
        self.feature_columns = None

        if os.path.exists(model_path) and os.path.exists(features_path):
            self.model = joblib.load(model_path)
            self.feature_columns = joblib.load(features_path)
        else:
            print(f"[WARNING] Model or feature artifacts missing ({model_path}). Running in heuristic fallback mode.")

    def predict(self, url: str) -> dict:
        """
        Predicts whether a URL is legitimate or potentially phishing.
        """
        raw_features = extract_url_features(url)

        if self.model is not None and self.feature_columns is not None:
            # Prepare aligned dataframe
            input_df = build_features_from_url(url, self.feature_columns)

            # In PhiUSIIL: class 0 is Phishing, class 1 is Legitimate
            probs = self.model.predict_proba(input_df)[0]
            # Classes might be [0, 1]
            classes = list(self.model.classes_)
            idx_0 = classes.index(0) if 0 in classes else 0
            prob_phishing = float(probs[idx_0])
            is_phishing = int(prob_phishing >= 0.5)
        else:
            # Heuristic calculation if model not yet trained
            heuristic_risk = 0.05
            if raw_features.get("IsDomainIP", 0) == 1:
                heuristic_risk += 0.40
            if raw_features.get("IsHTTPS", 0) == 0:
                heuristic_risk += 0.20
            if raw_features.get("HasObfuscation", 0) == 1:
                heuristic_risk += 0.20
            if raw_features.get("NoOfSubDomain", 0) >= 2:
                heuristic_risk += 0.15
            if raw_features.get("URLLength", 0) > 75:
                heuristic_risk += 0.15

            prob_phishing = min(max(heuristic_risk, 0.01), 0.99)
            is_phishing = int(prob_phishing >= 0.5)

        risk_percent = round(prob_phishing * 100, 2)
        prediction_label = "POTENTIAL PHISHING" if is_phishing else "LEGITIMATE"

        if risk_percent >= 70:
            risk_level = "High"
        elif risk_percent >= 40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Key characteristics breakdown for presentation
        characteristics = {
            "url_length": "High" if raw_features.get("url_length", 0) > 75 else "Normal",
            "special_characters": "High" if raw_features.get("num_special_chars", 0) > 10 else "Normal",
            "subdomains": "High" if raw_features.get("num_subdomains", 0) >= 2 else "Normal",
            "ip_address": "Detected" if raw_features.get("has_ip", 0) == 1 else "Not detected",
            "https": "Detected" if raw_features.get("has_https", 0) == 1 else "Not detected",
        }

        return {
            "url": url,
            "prediction": prediction_label,
            "is_phishing": bool(is_phishing),
            "probability": prob_phishing,
            "risk_score": risk_percent,
            "risk_level": risk_level,
            "characteristics": characteristics,
            "raw_features": raw_features,
        }


def predict_url(url: str) -> dict:
    predictor = PhishingPredictor()
    return predictor.predict(url)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Predict if a URL is legitimate or fraudulent")
    parser.add_argument("--url", type=str, required=True, help="Website URL to inspect")
    args = parser.parse_args()

    result = predict_url(args.url)
    print("\n" + "=" * 50)
    print("        ANALYSIS RESULT")
    print("=" * 50)
    print(f"URL            : {result['url']}")
    print(f"Classification : {result['prediction']}")
    print(f"Risk Score     : {result['risk_score']}% ({result['risk_level']} Risk)")
    print("-" * 50)
    print("Characteristics Breakdown:")
    for k, v in result["characteristics"].items():
        print(f"  {k.replace('_', ' ').title():<22} : {v}")
    print("=" * 50)
