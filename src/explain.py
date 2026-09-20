"""
Explainability Module
Provides human-readable local explanations and global feature importance.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import joblib
import pandas as pd


def explain_prediction(features_dict: dict, top_n=5) -> list:
    """
    Generates human-readable explanations for why a URL was classified.
    """
    reasons = []

    if features_dict.get("has_ip", 0) == 1:
        reasons.append({"feature": "IP Address Hostname", "impact": "High Risk", "detail": "URL uses a raw numeric IP address instead of a registered domain name."})

    if features_dict.get("has_https", 0) == 0:
        reasons.append({"feature": "Missing HTTPS", "impact": "Moderate Risk", "detail": "Connection uses plain unencrypted HTTP, lacking TLS encryption."})

    if features_dict.get("has_at", 0) == 1:
        reasons.append({"feature": "@ Symbol Obfuscation", "impact": "High Risk", "detail": "Contains '@' symbol, often used to bypass domain inspection."})

    if features_dict.get("num_subdomains", 0) >= 2:
        reasons.append({"feature": "Excessive Subdomains", "impact": "Moderate Risk", "detail": f"Contains {features_dict.get('num_subdomains')} subdomains, commonly used to impersonate reputable brands."})

    if features_dict.get("url_length", 0) > 75:
        reasons.append({"feature": "Abnormal URL Length", "impact": "Moderate Risk", "detail": f"URL length ({features_dict.get('url_length')} characters) is unusually long."})

    if features_dict.get("suspicious_keyword_count", 0) > 0:
        reasons.append({"feature": "Targeted Keywords Detected", "impact": "High Risk", "detail": "Contains sensitive authentication words (login, verify, secure, banking)."})

    if features_dict.get("num_special_chars", 0) > 12:
        reasons.append({"feature": "High Special Characters", "impact": "Moderate Risk", "detail": f"Contains {features_dict.get('num_special_chars')} non-alphanumeric characters."})

    if not reasons:
        reasons.append({"feature": "Standard Clean Lexical Profile", "impact": "Safe", "detail": "HTTPS enabled, legitimate domain structure, no obfuscation indicators."})

    return reasons[:top_n]


def get_global_feature_importance(model_path="models/xgboost_fraud_detector.pkl", features_path="models/feature_columns.pkl"):
    if not (os.path.exists(model_path) and os.path.exists(features_path)):
        return None
    model = joblib.load(model_path)
    feature_columns = joblib.load(features_path)
    return pd.Series(model.feature_importances_, index=feature_columns).sort_values(ascending=False)
