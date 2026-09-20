"""
Flask Web Application for Real-Time Fraudulent Website Detection
Provides web dashboard and JSON REST API for URL classification.
"""

import os
import sys

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask, render_template, request, jsonify
from src.predict import PhishingPredictor
from src.explain import explain_prediction

app = Flask(__name__)

# Initialize predictor
predictor = PhishingPredictor()


@app.route("/")
def home():
    """Renders the main detection dashboard."""
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict_endpoint():
    """
    Accepts JSON: {"url": "https://..."}
    Returns analysis result with classification, risk score, characteristics, and explanations.
    """
    data = request.get_json(silent=True) or {}
    url = data.get("url", "").strip()

    if not url:
        return jsonify({"error": "Please provide a valid website URL."}), 400

    try:
        result = predictor.predict(url)
        # Add explanation details
        result["explanations"] = explain_prediction(result["raw_features"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Prediction failed: {str(e)}"}), 500


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "fraudulent-website-detection"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
