# Fraudulent Website Detection System using Machine Learning

AI-powered cybersecurity system designed to identify fraudulent and phishing websites using **XGBoost** with optional **NVIDIA GPU acceleration**.

---

## 1. Project Overview

Phishing attacks and fraudulent websites mimic legitimate platforms to harvest sensitive credentials, banking information, and private data. Static blocklists are insufficient against zero-hour threats. 

This project provides an end-to-end, hackathon-ready solution that:
- Ingests website/URL characteristics.
- Analyzes structural, lexical, and security indicators.
- Classifies URLs as **Legitimate** or **Potential Phishing** using an **XGBoost Classifier**.
- Estimates risk probabilities and explains reasons behind classification.
- Features a real-time web application dashboard for live demonstrations.

---

## 2. Project Architecture

```text
               +----------------------------------+
               |        USER / CLIENT APP         |
               |       (Enter Website URL)        |
               +----------------+-----------------+
                                |
                                v
               +----------------------------------+
               |      URL Feature Extraction      |
               | (Length, IP, Subdomains, HTTPS)  |
               +----------------+-----------------+
                                |
                                v
               +----------------------------------+
               |        Data Preprocessing        |
               |     & Alignment with Schema      |
               +----------------+-----------------+
                                |
                                v
               +----------------------------------+
               |       XGBoost Classifier         |
               | (Optional NVIDIA CUDA / hist)    |
               +----------------+-----------------+
                                |
            +-------------------+-------------------+
            |                                       |
            v                                       v
    [ LEGITIMATE ]                         [ POTENTIAL PHISHING ]
            |                                       |
            +-------------------+-------------------+
                                |
                                v
               +----------------------------------+
               |   Risk Probability & Indicators  |
               |   Explainability (SHAP / Tree)   |
               +----------------+-----------------+
                                |
                                v
               +----------------------------------+
               |       Flask Web Dashboard        |
               +----------------------------------+
```

---

## 3. Project Directory Structure

```text
fraudulent-website-detection/
|
+-- data/
|   +-- raw/                  # Raw dataset (e.g., phiusiil.csv)
|   +-- processed/            # Train and test splits (train.csv, test.csv)
|   +-- external/             # Independent evaluation sets (phishtank.csv, tranco.csv)
|
+-- notebooks/
|   +-- 01_EDA.ipynb          # Exploratory Data Analysis & visual inspections
|
+-- src/
|   +-- __init__.py           # Package marker
|   +-- download_dataset.py   # Fetches PhiUSIIL dataset from UCI Repository (ID: 967)
|   +-- analyze_data.py       # Data validation, schema analysis, missing value checks
|   +-- preprocessing.py      # Cleans and stratifies data into 80/20 train/test splits
|   +-- feature_engineering.py# Aligns inference features with training schema
|   +-- url_features.py       # Extracts lexical, syntactic, and security features from URLs
|   +-- train_model.py        # Trains XGBoost model (supports CPU and NVIDIA GPU)
|   +-- evaluate_model.py     # Generates evaluation metrics, confusion matrix, ROC curve
|   +-- predict.py            # Real-time inference engine
|   +-- explain.py            # Decision explainability and risk factor attribution
|
+-- models/
|   +-- xgboost_fraud_detector.pkl  # Trained serialized XGBoost classifier
|   +-- feature_columns.pkl         # Serialized list of model feature columns
|
+-- results/
|   +-- figures/              # Saved charts (confusion_matrix.png, roc_curve.png, etc.)
|   +-- metrics/              # Saved evaluation scores (model_comparison.csv)
|
+-- app/
|   +-- __init__.py           # Flask app package marker
|   +-- app.py                # Flask server application
|   +-- templates/
|   |   +-- index.html        # Web dashboard interface
|   +-- static/
|       +-- style.css         # Modern cybersecurity dashboard styling
|       +-- script.js         # Client AJAX handler and dynamic UI renderer
|
+-- requirements.txt          # Python dependencies
+-- run_app.py                # Main script to run web server
+-- README.md                 # Project documentation
```

---

## 4. Environment Setup

### 1. Create Virtual Environment
```powershell
# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies
```powershell
pip install -r requirements.txt
```

---

## 5. End-to-End Pipeline Execution

### Step 1: Download the Dataset
Fetches the PhiUSIIL Phishing URL Dataset (UCI ID 967):
```powershell
python src/download_dataset.py
```

### Step 2: Inspect and Analyze Dataset
Inspects schema, datatypes, missing values, duplicates, and class balance:
```powershell
python src/analyze_data.py
```

### Step 3: Preprocess Data
Performs data cleaning, feature separation, and stratified train/test split:
```powershell
python src/preprocessing.py
```

### Step 4: Train the XGBoost Classifier
Train baseline on CPU:
```powershell
python src/train_model.py
```

Train with **NVIDIA GPU Acceleration (CUDA)**:
```powershell
python src/train_model.py --gpu
```

### Step 5: Evaluate the Model & Generate PPT Figures
Computes accuracy, precision, recall, F1, ROC-AUC, and generates visual charts in `results/figures/`:
```powershell
python src/evaluate_model.py
```

### Step 6: Test Single URL via CLI
```powershell
python src/predict.py --url "https://example.com"
```

### Step 7: Launch the Web Application
```powershell
python run_app.py
```
Open **http://127.0.0.1:5000** in your browser.

---

## 6. Key Features Extracted from URLs

| Feature | Description |
|---|---|
| `url_length` | Total character count of the URL |
| `domain_length` | Length of hostname / domain |
| `num_digits` | Total count of numerical digits |
| `num_special_chars` | Count of special / non-alphanumeric characters |
| `num_subdomains` | Number of subdomains extracted from domain |
| `has_ip` | Flag indicates whether hostname is an IP address |
| `has_https` | Flag indicates whether URL uses secure HTTPS protocol |
| `has_at` | Flag indicates presence of `@` obfuscation symbol |
| `suspicious_keywords` | Detection of sensitive authentication keywords |

---

## 7. Presentation Artifacts
Generated visual artifacts ready for PPT slides:
- `results/figures/confusion_matrix.png`
- `results/figures/roc_curve.png`
- `results/figures/feature_importance.png`
- `results/metrics/model_comparison.csv`
