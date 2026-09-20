"""
Main Entry Point to Launch the Flask Web Application
Usage:
    python run_app.py
"""

from app.app import app

if __name__ == "__main__":
    print("=" * 60)
    print("Fraudulent Website Detection System - Web Interface")
    print("Powered by XGBoost & Machine Learning")
    print("=" * 60)
    print("Starting server on: http://127.0.0.1:5000")
    print("Press CTRL+C to stop the server.")
    app.run(host="0.0.0.0", port=5000, debug=True)
