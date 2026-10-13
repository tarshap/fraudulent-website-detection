"""
Main Entry Point to Launch the Web Application
Supports both:
  - Streamlit: streamlit run streamlit_app.py (or streamlit run run_app.py)
  - Flask:     python run_app.py
"""

import sys
import os

# Detect if executed via Streamlit CLI (e.g. `streamlit run run_app.py`)
_is_streamlit = False
try:
    from streamlit.runtime.scriptrunner import get_script_run_ctx
    if get_script_run_ctx() is not None:
        _is_streamlit = True
except Exception:
    pass

if _is_streamlit:
    # Seamlessly forward to Streamlit application
    import streamlit_app
else:
    from app.app import app

    if __name__ == "__main__":
        print("=" * 60)
        print("Fraudulent Website Detection System - Web Interface (Flask)")
        print("Powered by XGBoost & Machine Learning")
        print("=" * 60)
        print("Starting Flask server on: http://127.0.0.1:5000")
        print("Tip: To run the Streamlit UI, execute:")
        print("     streamlit run streamlit_app.py")
        print("=" * 60)
        print("Press CTRL+C to stop the server.")
        app.run(host="0.0.0.0", port=5000, debug=False)
