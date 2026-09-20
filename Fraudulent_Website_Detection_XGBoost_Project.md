# Fraudulent Website Detection System using Machine Learning

## 1. Project Overview

This project develops a **Fraudulent Website / Phishing Website Detection System using Machine Learning**.

The system analyzes website and URL characteristics and uses an **XGBoost binary classifier** to classify a website as:

- **Legitimate**
- **Potentially Fraudulent / Phishing**

The project is designed as a hackathon-ready solution with:

- A large public phishing dataset
- Data preprocessing and exploratory analysis
- XGBoost model training
- Model evaluation
- Feature importance and explainability
- Optional NVIDIA GPU acceleration
- A real-time URL prediction web application
- PPT-ready charts and screenshots

---

## 2. Problem Statement

Fraudulent and phishing websites are commonly used to steal:

- Usernames and passwords
- Banking information
- Credit/debit card details
- Personal information
- Authentication credentials

Traditional blocklists cannot identify every newly created malicious website.

This project uses machine learning to identify suspicious websites based on measurable characteristics of their URLs and website-related features.

### Objective

Build a machine learning system that:

1. Accepts website/URL characteristics as input.
2. Extracts and preprocesses relevant features.
3. Uses XGBoost for binary classification.
4. Predicts whether the website is legitimate or potentially phishing.
5. Provides a model probability/risk indication.
6. Shows important characteristics contributing to the prediction.
7. Provides a simple web interface for a hackathon demonstration.

---

# 3. Proposed Solution

The proposed solution is:

```text
                    USER
                      |
                      v
              Enter Website URL
                      |
                      v
            URL Feature Extraction
                      |
                      v
              Data Preprocessing
                      |
                      v
             XGBoost Classifier
                      |
                      v
          +-----------+-----------+
          |                       |
          v                       v
     LEGITIMATE             POTENTIAL PHISHING
          |                       |
          +-----------+-----------+
                      |
                      v
             Risk / Probability
                      |
                      v
             Explain Prediction
                      |
                      v
               Web Dashboard
```

---

# 4. Dataset

## Primary Dataset: PhiUSIIL

The primary training dataset is the **PhiUSIIL Phishing URL (Website) Dataset** from the UCI Machine Learning Repository.

Dataset page:

https://archive.ics.uci.edu/dataset/967/phiusiil%2Bphishing%2Burl%2Bdataset

The dataset contains approximately:

- 235,795 website records
- 54 features
- Legitimate and phishing examples
- URL-related and website-related characteristics

The exact number of records and columns should be verified after downloading the dataset because the project should use the actual downloaded schema rather than hard-coded assumptions.

---

# 5. Dataset Characteristics

The dataset contains characteristics related to URL and website structure.

Typical feature categories include:

### URL characteristics

- URL length
- Number of letters
- Number of digits
- Number of special characters
- URL structure

### Domain characteristics

- Domain length
- Subdomain characteristics
- Domain/IP information
- TLD-related information

### Security-related characteristics

- HTTPS information
- Redirect characteristics
- Suspicious URL patterns

### Website characteristics

Additional website/page-level characteristics are available in the PhiUSIIL dataset.

---

# 6. Project Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | XGBoost |
| ML Utilities | Scikit-learn |
| Visualization | Matplotlib, Seaborn |
| Explainability | XGBoost Feature Importance / SHAP |
| Model Serialization | Joblib |
| Web Application | Flask |
| Frontend | HTML, CSS, JavaScript |
| Optional GPU Acceleration | NVIDIA CUDA + GPU-enabled XGBoost |
| Dataset | UCI PhiUSIIL |

---

# 7. NVIDIA Component

The primary machine learning algorithm is **XGBoost**.

For NVIDIA-enabled environments, XGBoost can be configured to use a CUDA-capable GPU where supported by the installed XGBoost version.

The NVIDIA component is used primarily for:

- GPU-accelerated model training
- Faster large-scale model experimentation
- Measuring CPU vs GPU training performance

The project should report **actual measured acceleration**, rather than assuming a particular speedup.

---

# 8. Why XGBoost?

XGBoost is appropriate because the dataset is primarily structured/tabular data.

Advantages include:

- Strong performance on tabular datasets
- Handles nonlinear relationships
- Handles feature interactions
- Provides feature importance
- Supports probability prediction
- Supports GPU acceleration
- Works well with binary classification
- Mature Python ecosystem

The model objective is:

```text
Legitimate  <---->  Potential Phishing
```

---

# 9. Project Architecture

```text
                         +-------------------+
                         |       USER        |
                         |    Enter URL      |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | URL Feature       |
                         | Extraction        |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | Preprocessing     |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | NVIDIA GPU        |
                         | Optional CUDA     |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | XGBoost           |
                         | Binary Classifier |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | Prediction +      |
                         | Model Probability |
                         +---------+---------+
                                   |
                    +--------------+--------------+
                    |                             |
                    v                             v
              LEGITIMATE                  POTENTIAL PHISHING
                    |                             |
                    +--------------+--------------+
                                   |
                                   v
                         +-------------------+
                         | Explainability    |
                         | Feature Importance|
                         | / SHAP            |
                         +---------+---------+
                                   |
                                   v
                         +-------------------+
                         | Web Dashboard     |
                         +-------------------+
```

---

# 10. Project Folder Structure

The recommended project structure is:

```text
fraudulent-website-detection/
|
+-- data/
|   +-- raw/
|   |   +-- phiusiil.csv
|   |
|   +-- processed/
|   |
|   +-- external/
|       +-- phishtank.csv
|       +-- tranco.csv
|
+-- notebooks/
|   +-- 01_EDA.ipynb
|
+-- src/
|   +-- download_dataset.py
|   +-- analyze_data.py
|   +-- preprocessing.py
|   +-- feature_engineering.py
|   +-- train_model.py
|   +-- evaluate_model.py
|   +-- predict.py
|   +-- url_features.py
|   +-- explain.py
|
+-- models/
|   +-- xgboost_fraud_detector.pkl
|   +-- feature_columns.pkl
|
+-- results/
|   +-- figures/
|   |   +-- class_distribution.png
|   |   +-- confusion_matrix.png
|   |   +-- roc_curve.png
|   |   +-- feature_importance.png
|   |
|   +-- metrics/
|       +-- model_comparison.csv
|
+-- app/
|   +-- app.py
|   +-- templates/
|   |   +-- index.html
|   |
|   +-- static/
|       +-- style.css
|       +-- script.js
|
+-- requirements.txt
+-- README.md
+-- run_app.py
```

---

# 11. Environment Setup

Create a Python virtual environment.

## Windows

```powershell
python -m venv venv
```

Activate:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install pandas numpy scikit-learn xgboost matplotlib seaborn joblib ucimlrepo flask shap
```

Save dependencies:

```powershell
pip freeze > requirements.txt
```

Verify XGBoost:

```powershell
python -c "import xgboost; print(xgboost.__version__)"
```

---

# 12. Download Dataset

Create:

```text
src/download_dataset.py
```

Example:

```python
from ucimlrepo import fetch_ucirepo
import pandas as pd
import os

print("Downloading PhiUSIIL dataset...")

dataset = fetch_ucirepo(id=967)

X = dataset.data.features
y = dataset.data.targets

print("Feature shape:", X.shape)
print("Target shape:", y.shape)

print("\nFeature columns:")
print(X.columns.tolist())

print("\nTarget columns:")
print(y.columns.tolist())

df = pd.concat([X, y], axis=1)

os.makedirs("data/raw", exist_ok=True)

output_file = "data/raw/phiusiil.csv"

df.to_csv(output_file, index=False)

print("\nSaved:", output_file)
print("Final shape:", df.shape)
```

Run:

```powershell
python src/download_dataset.py
```

---

# 13. Dataset Inspection

Before model training, inspect the actual downloaded schema.

```python
import pandas as pd

df = pd.read_csv("data/raw/phiusiil.csv")

print("Shape:", df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())
```

The target column must be confirmed from the downloaded dataset.

Do not assume the target column name without checking the actual file.

---

# 14. Data Cleaning

The preprocessing stage should:

1. Identify the target column.
2. Separate target from input features.
3. Inspect missing values.
4. Remove or handle duplicates as appropriate.
5. Identify raw text columns.
6. Identify numeric features.
7. Handle categorical features if required.
8. Preserve the feature schema used by the model.

Conceptually:

```python
X = df.drop(columns=[TARGET])
y = df[TARGET]
```

Raw fields such as complete URL strings or domain strings should not automatically be fed directly into XGBoost.

For the initial structured-data model, use the numerical/categorical features that are consistently available.

---

# 15. Train/Test Split

Use a stratified split:

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)
```

This creates approximately:

```text
80% Training
20% Testing
```

The random seed provides reproducibility.

---

# 16. Initial XGBoost Model

Start with a baseline model:

```python
from xgboost import XGBClassifier

model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=-1
)

model.fit(
    X_train,
    y_train
)
```

These parameters are a starting point and should be tuned based on validation results.

---

# 17. Evaluation Metrics

Do not evaluate the model using accuracy alone.

Calculate:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix

Example:

```python
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report
)

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, pred)

precision = precision_score(y_test, pred)

recall = recall_score(y_test, pred)

f1 = f1_score(y_test, pred)

auc = roc_auc_score(y_test, prob)

print("Accuracy :", accuracy)
print("Precision:", precision)
print("Recall   :", recall)
print("F1       :", f1)
print("ROC-AUC  :", auc)

print(
    classification_report(
        y_test,
        pred
    )
)
```

The actual values must be generated from the trained model.

---

# 18. Confusion Matrix

Generate:

```python
from sklearn.metrics import ConfusionMatrixDisplay
import matplotlib.pyplot as plt

ConfusionMatrixDisplay.from_predictions(
    y_test,
    pred
)

plt.title(
    "XGBoost Fraudulent Website Detection"
)

plt.savefig(
    "results/figures/confusion_matrix.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

The confusion matrix contains:

```text
                 Predicted
              Legitimate  Phishing

Actual
Legitimate        TN         FP

Phishing          FN         TP
```

---

# 19. ROC Curve

Generate:

```python
from sklearn.metrics import RocCurveDisplay
import matplotlib.pyplot as plt

RocCurveDisplay.from_predictions(
    y_test,
    prob
)

plt.title(
    "XGBoost ROC Curve"
)

plt.savefig(
    "results/figures/roc_curve.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
```

---

# 20. Feature Importance

XGBoost provides feature importance.

```python
import pandas as pd
import matplotlib.pyplot as plt

importance = pd.Series(
    model.feature_importances_,
    index=X_train.columns
)

importance = importance.sort_values(
    ascending=False
)

print(importance.head(20))
```

Plot:

```python
importance.head(20).sort_values().plot(
    kind="barh"
)

plt.title(
    "Top Features Used by XGBoost"
)

plt.tight_layout()

plt.savefig(
    "results/figures/feature_importance.png",
    dpi=300
)

plt.show()
```

This provides a useful explanation of which features the model relied on most across the dataset.

---

# 21. Save the Model

Save the trained model:

```python
import joblib

joblib.dump(
    model,
    "models/xgboost_fraud_detector.pkl"
)
```

Save the exact feature order:

```python
joblib.dump(
    list(X_train.columns),
    "models/feature_columns.pkl"
)
```

The feature order must remain identical during inference.

---

# 22. NVIDIA GPU Acceleration

After the CPU implementation is working correctly, test GPU acceleration.

Check the NVIDIA GPU:

```powershell
nvidia-smi
```

For a compatible XGBoost installation, a GPU configuration can use:

```python
model = XGBClassifier(
    n_estimators=300,
    max_depth=8,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    objective="binary:logistic",
    eval_metric="logloss",
    tree_method="hist",
    device="cuda",
    random_state=42
)
```

The exact GPU parameters depend on the installed XGBoost version.

Always verify the installed XGBoost documentation/version before finalizing the GPU configuration.

---

# 23. NVIDIA Acceleration Experiment

Measure CPU and GPU training times.

Example methodology:

```text
CPU XGBoost
     |
     +-- Training time = measured value

GPU XGBoost
     |
     +-- Training time = measured value
```

Calculate:

```text
GPU Speedup =
CPU Training Time / GPU Training Time
```

Only report the actual measured value.

Recommended PPT table:

| Configuration | Training Time | Accuracy | F1 | ROC-AUC |
|---|---:|---:|---:|---:|
| XGBoost CPU | Actual | Actual | Actual | Actual |
| XGBoost NVIDIA GPU | Actual | Actual | Actual | Actual |

---

# 24. URL Feature Extraction

For the real-time application, URL-level characteristics can be extracted using Python.

Potential features include:

- URL length
- Domain length
- Number of digits
- Number of letters
- Number of dots
- Number of hyphens
- Number of slashes
- Number of special characters
- Presence of `@`
- HTTPS presence
- Query parameter count
- Subdomain count
- IP address presence

Example:

```python
from urllib.parse import urlparse
import ipaddress


def extract_url_features(url):

    parsed = urlparse(url)

    hostname = parsed.netloc

    features = {}

    features["url_length"] = len(url)

    features["domain_length"] = len(hostname)

    features["num_digits"] = sum(
        c.isdigit()
        for c in url
    )

    features["num_letters"] = sum(
        c.isalpha()
        for c in url
    )

    features["num_dots"] = url.count(".")

    features["num_hyphens"] = url.count("-")

    features["num_slashes"] = url.count("/")

    features["num_special_chars"] = sum(
        not c.isalnum()
        for c in url
    )

    features["has_at"] = int(
        "@" in url
    )

    features["has_https"] = int(
        parsed.scheme == "https"
    )

    features["num_query_params"] = (
        len(parsed.query.split("&"))
        if parsed.query
        else 0
    )

    features["num_subdomains"] = max(
        hostname.count(".") - 1,
        0
    )

    try:
        ipaddress.ip_address(hostname)
        features["has_ip"] = 1
    except ValueError:
        features["has_ip"] = 0

    return features
```

## Important

The live URL feature extractor must generate the **same feature representation expected by the trained XGBoost model**.

If the training model uses the 54 PhiUSIIL features, the live application cannot provide only 12 unrelated features.

Therefore, the final implementation should either:

1. Train a model specifically on the handcrafted URL features used by the application, or
2. Reproduce the required PhiUSIIL feature extraction pipeline.

For a reliable hackathon MVP, option 1 is often simpler for real-time URL input.

---

# 25. Real-Time Prediction

The application flow is:

```text
User enters URL
       |
       v
Feature extraction
       |
       v
Feature alignment
       |
       v
XGBoost model
       |
       +---- Prediction
       |
       +---- Model probability
       |
       v
Risk interpretation
```

Example output:

```text
Prediction: Potential Phishing
Model probability: 93%
```

The displayed probability is the model's estimated class probability, not proof that the website is malicious.

---

# 26. Explainability

The application can show:

```text
WHY WAS THIS URL FLAGGED?

URL Length              High
Special Characters      High
Subdomains              High
IP Address              Detected
HTTPS                    Not detected
Domain Structure         Suspicious
```

For global explanations use XGBoost feature importance.

For per-prediction explanations, SHAP can be used:

```python
import shap

explainer = shap.TreeExplainer(model)

shap_values = explainer(X)
```

---

# 27. Flask Web Application

Create:

```text
app/app.py
```

Basic architecture:

```python
from flask import Flask, render_template, request, jsonify
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load(
    "models/xgboost_fraud_detector.pkl"
)

feature_columns = joblib.load(
    "models/feature_columns.pkl"
)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():

    data = request.get_json()

    url = data.get("url")

    # Extract URL features.
    # Align features with the model.
    # Generate prediction.

    return jsonify({
        "prediction": "...",
        "probability": 0.0
    })


if __name__ == "__main__":
    app.run(debug=True)
```

The prediction logic should be connected to the same feature engineering pipeline used during training.

---

# 28. Web Application UI

The main page should contain:

```text
====================================================

       FRAUDULENT WEBSITE DETECTION SYSTEM

       AI-powered website security using XGBoost

       Enter Website URL

       +------------------------------------------+
       | https://example.com                      |
       +------------------------------------------+

                 [ ANALYZE WEBSITE ]

====================================================
```

After analysis:

```text
====================================================

                 ANALYSIS RESULT

             POTENTIAL PHISHING

                  Risk: XX%

----------------------------------------------------

URL Characteristics

URL Length                  High
Special Characters          High
Subdomains                   High
IP Address                   Detected
HTTPS                        Not detected

----------------------------------------------------

Model: XGBoost
Classification: Potential Phishing

====================================================
```

The actual prediction and probability must come from the trained model.

---

# 29. External Validation

After the initial model is working, use an independent dataset/source for additional validation.

### PhishTank

PhishTank provides verified phishing URL information and downloadable feeds.

https://phishtank.org/developer_info.php

Use this as an external phishing validation source.

### Legitimate Domains

A source such as Tranco can be used for legitimate-domain validation.

The validation architecture becomes:

```text
                  TRAIN
                    |
                    v
                PhiUSIIL
                    |
                    v
                 XGBoost
                    |
          +---------+---------+
          |                   |
          v                   v
     Internal Test      External Validation
                              |
                    +---------+---------+
                    |                   |
                    v                   v
                PhishTank           Legitimate
```

Do not automatically merge external validation data into the training set.

Keep it separate when measuring independent generalization.

---

# 30. Experiments

The final project should include these experiments.

## Experiment 1 — Baseline XGBoost

Use the selected dataset features.

Measure:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC

## Experiment 2 — Hyperparameter Tuning

Tune:

- `n_estimators`
- `max_depth`
- `learning_rate`
- `subsample`
- `colsample_bytree`

## Experiment 3 — Explainability

Generate:

- Feature importance
- SHAP analysis

## Experiment 4 — NVIDIA Acceleration

Compare:

- CPU XGBoost
- NVIDIA GPU XGBoost

## Experiment 5 — External Validation

Evaluate against independent phishing/legitimate URL data.

---

# 31. Results Files for PPT

The project should generate:

```text
results/
|
+-- figures/
|   +-- class_distribution.png
|   +-- confusion_matrix.png
|   +-- roc_curve.png
|   +-- feature_importance.png
|
+-- metrics/
    +-- model_metrics.csv
    +-- cpu_gpu_comparison.csv
```

These can be directly used in the hackathon presentation.

---

# 32. Suggested PPT Slides

## Slide 1 — Title

**Fraudulent Website Detection System using Machine Learning**

Subtitle:

**XGBoost-Based Phishing Website Detection with NVIDIA GPU Acceleration**

---

## Slide 2 — Problem

Explain:

- Growth of phishing/fraudulent websites
- New malicious domains appear frequently
- Static blocklists have limitations
- Need for automated risk assessment

---

## Slide 3 — Proposed Solution

```text
URL
 ↓
Feature Extraction
 ↓
Preprocessing
 ↓
XGBoost
 ↓
Risk Prediction
 ↓
Explainability
```

---

## Slide 4 — Dataset

Show:

- Dataset name
- Number of records
- Number of features
- Legitimate count
- Phishing count

Use the actual downloaded dataset values.

---

## Slide 5 — Feature Engineering

Show:

```text
URL Length
Domain Length
Special Characters
IP Address
HTTPS
Subdomains
Redirect Characteristics
Website Characteristics
```

---

## Slide 6 — XGBoost Model

Explain:

- Binary classification
- Gradient boosted decision trees
- Nonlinear relationships
- Feature importance
- Probability prediction

---

## Slide 7 — Model Results

Insert:

`results/figures/confusion_matrix.png`

and:

`results/figures/roc_curve.png`

---

## Slide 8 — Feature Importance

Insert:

`results/figures/feature_importance.png`

Explain the top features discovered by the trained model.

---

## Slide 9 — NVIDIA Acceleration

Show:

```text
CPU XGBoost
Training Time: Actual

NVIDIA GPU XGBoost
Training Time: Actual

Measured Speedup: Actual
```

Also mention the NVIDIA GPU/CUDA configuration actually used.

---

## Slide 10 — Application

Screenshot of the Flask web application.

---

## Slide 11 — Live Demo

Demonstrate:

1. Enter URL
2. Analyze
3. Show classification
4. Show probability
5. Show risk indicators
6. Show explanation

---

## Slide 12 — Conclusion

Highlight:

- Automated phishing detection
- ML-based classification
- XGBoost
- Explainable results
- NVIDIA GPU acceleration
- Real-time URL analysis

---

# 33. Recommended Final Demo Screenshot

The most important screenshot for the PPT should be the final application screen:

```text
+------------------------------------------------------+
|                                                      |
|       FRAUDULENT WEBSITE DETECTION SYSTEM            |
|                                                      |
|       Powered by XGBoost                             |
|                                                      |
|       Website URL                                    |
|       +------------------------------------------+   |
|       | <URL entered by user>                    |   |
|       +------------------------------------------+   |
|                                                      |
|                [ ANALYZE WEBSITE ]                   |
|                                                      |
|       --------------------------------------------   |
|                                                      |
|                  ANALYSIS RESULT                     |
|                                                      |
|              POTENTIAL PHISHING                      |
|                                                      |
|              Risk Score: XX%                         |
|                                                      |
|       URL Length             XX                      |
|       Special Characters    XX                       |
|       Subdomains             XX                      |
|       IP Address             XX                      |
|       HTTPS                  XX                      |
|                                                      |
|       Model: XGBoost                                 |
|                                                      |
+------------------------------------------------------+
```

Use a safe test/validation URL for the demonstration. Do not visit or interact with an actual malicious website merely to generate a screenshot.

---

# 34. Important Evaluation Rules

Do not:

- Invent accuracy values.
- Invent GPU speedup.
- Use test data during training.
- Leak the target column into features.
- Claim that a model can detect every fraudulent website.
- Treat a model probability as definitive proof of fraud.
- Mix external validation data into training without documenting it.

Do:

- Report actual measured metrics.
- Preserve train/test separation.
- Check duplicates.
- Check class distribution.
- Check feature leakage.
- Report false positives and false negatives.
- Record the exact dataset version/source.
- Record the XGBoost version.
- Record the GPU/CUDA environment if GPU acceleration is used.

---

# 35. Final End-to-End Workflow

```text
STEP 1
Create Python environment
        |
        v
STEP 2
Install dependencies
        |
        v
STEP 3
Download PhiUSIIL
        |
        v
STEP 4
Inspect dataset
        |
        v
STEP 5
Clean data
        |
        v
STEP 6
Select features
        |
        v
STEP 7
Train/Test split
        |
        v
STEP 8
Train XGBoost CPU
        |
        v
STEP 9
Evaluate model
        |
        +---- Accuracy
        +---- Precision
        +---- Recall
        +---- F1
        +---- ROC-AUC
        +---- Confusion Matrix
        |
        v
STEP 10
Feature Importance
        |
        v
STEP 11
Hyperparameter tuning
        |
        v
STEP 12
Save final model
        |
        v
STEP 13
Enable NVIDIA GPU
        |
        v
STEP 14
Measure CPU vs GPU
        |
        v
STEP 15
Build URL feature extractor
        |
        v
STEP 16
Build prediction pipeline
        |
        v
STEP 17
Build Flask application
        |
        v
STEP 18
Add explainability
        |
        v
STEP 19
External validation
        |
        v
STEP 20
Generate PPT charts
        |
        v
STEP 21
Capture final application screenshot
        |
        v
STEP 22
Prepare hackathon presentation
```

---

# 36. Final Deliverable

The completed hackathon project should demonstrate:

**Input**

```text
Website URL
```

**Processing**

```text
URL Feature Extraction
        ↓
Preprocessing
        ↓
XGBoost
        ↓
NVIDIA GPU acceleration (optional/where supported)
```

**Output**

```text
Legitimate / Potential Phishing
+
Model Probability
+
Risk Indicators
+
Feature Explanation
```

**Evidence**

```text
Confusion Matrix
ROC Curve
Feature Importance
Evaluation Metrics
External Validation
CPU vs GPU Timing
```

This provides both a **working ML project** and the **visual evidence needed for a hackathon PPT**.
