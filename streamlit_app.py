"""
Streamlit Web Application for Real-Time Fraudulent Website Detection
Powered by XGBoost Machine Learning and Explainability Framework
"""

import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import streamlit as st
import pandas as pd
from PIL import Image

from src.predict import PhishingPredictor
from src.explain import explain_prediction
from src.url_features import extract_url_features

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Fraudulent Website Detection | AI Security",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# Custom Styling (Cybersecurity Theme)
# ---------------------------------------------------------
st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
    }
    .stApp {
        background-color: #0b0f19;
        color: #f3f4f6;
    }
    .header-box {
        background: linear-gradient(135deg, rgba(30, 58, 138, 0.4) 0%, rgba(17, 24, 39, 0.8) 100%);
        border: 1px solid #1e3a8a;
        padding: 1.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .header-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.3rem;
        letter-spacing: -0.02em;
    }
    .header-sub {
        font-size: 1.05rem;
        color: #93c5fd;
    }
    .badge-pill {
        display: inline-block;
        font-size: 0.75rem;
        font-family: monospace;
        padding: 0.25rem 0.75rem;
        background: rgba(59, 130, 246, 0.2);
        color: #60a5fa;
        border: 1px solid #3b82f6;
        border-radius: 9999px;
        margin-bottom: 0.5rem;
    }
    .status-card-phishing {
        background: rgba(239, 68, 68, 0.12);
        border: 2px solid #ef4444;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(239, 68, 68, 0.25);
    }
    .status-card-legit {
        background: rgba(16, 185, 129, 0.12);
        border: 2px solid #10b981;
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.25);
    }
    .char-metric-box {
        background: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 0.85rem;
        text-align: center;
    }
    .reason-box-high {
        background: #111827;
        border-left: 4px solid #ef4444;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .reason-box-mod {
        background: #111827;
        border-left: 4px solid #f59e0b;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
    .reason-box-safe {
        background: #111827;
        border-left: 4px solid #10b981;
        padding: 0.75rem 1rem;
        border-radius: 6px;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------
# Load Cached Predictor
# ---------------------------------------------------------
@st.cache_resource
def get_predictor():
    return PhishingPredictor()

predictor = get_predictor()

# Initialize session state for URL
if "input_url" not in st.session_state:
    st.session_state["input_url"] = "https://www.google.com"

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------
with st.sidebar:
    st.markdown("### 🛡️ System Overview")
    st.caption("AI-powered real-time detection of fraudulent and phishing websites using XGBoost.")
    
    st.markdown("---")
    st.markdown("#### ⚡ Model Specs")
    st.markdown("""
    - **Algorithm**: XGBoost (`hist` tree method)
    - **Dataset**: UCI PhiUSIIL (235,795 records)
    - **Training Time**: 0.49s on CPU
    - **Test Accuracy**: **99.60%**
    - **ROC-AUC**: **0.9984**
    """)

    st.markdown("---")
    st.markdown("#### 🧪 Quick Test Samples")
    
    if st.button("🟢 Safe: Google"):
        st.session_state["input_url"] = "https://www.google.com"
        st.rerun()

    if st.button("🟢 Safe: GitHub"):
        st.session_state["input_url"] = "https://www.github.com"
        st.rerun()

    if st.button("🔴 Phishing: IP & Sensitive Keywords"):
        st.session_state["input_url"] = "http://192.168.1.1/update-account/bank-verify-secure"
        st.rerun()

    if st.button("🔴 Phishing: Subdomain Spoofing"):
        st.session_state["input_url"] = "http://secure-paypal-login.account-verification-alert.com/signin"
        st.rerun()

    if st.button("🔴 Phishing: PhiUSIIL Benchmark URL"):
        st.session_state["input_url"] = "http://www.shprakserf.gq"
        st.rerun()

    st.markdown("---")
    st.caption("Hackathon Secured ML Project | 2026")


# ---------------------------------------------------------
# Header Banner
# ---------------------------------------------------------
st.markdown("""
<div class="header-box">
    <div class="badge-pill">XGBOOST CYBER DEFENSE</div>
    <div class="header-title">Fraudulent Website Detection System</div>
    <div class="header-sub">Real-Time Machine Learning Website Security & Explainable Risk Scoring</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Navigation Tabs
# ---------------------------------------------------------
tab_scan, tab_metrics, tab_batch = st.tabs([
    "🔍 Real-Time URL Scanner",
    "📊 Model Evaluation & PPT Visuals",
    "🧪 Batch URL Analysis"
])

# =========================================================
# TAB 1: Real-Time URL Scanner
# =========================================================
with tab_scan:
    st.markdown("##### Enter Website URL to Inspect:")
    
    col_input, col_btn = st.columns([5, 1])
    with col_input:
        target_url = st.text_input(
            label="Website URL",
            value=st.session_state["input_url"],
            placeholder="https://example.com/login",
            label_visibility="collapsed"
        )
    with col_btn:
        analyze_clicked = st.button("🚀 Analyze", use_container_width=True, type="primary")

    if target_url:
        st.session_state["input_url"] = target_url

    # Perform analysis
    if target_url and (analyze_clicked or target_url == st.session_state.get("last_scanned_url", "")):
        st.session_state["last_scanned_url"] = target_url
        with st.spinner("Analyzing lexical patterns, security indicators, and XGBoost probabilities..."):
            result = predictor.predict(target_url)
            explanations = explain_prediction(result["raw_features"])
            
            is_phishing = result["is_phishing"]
            risk_score = result["risk_score"]
            risk_level = result["risk_level"]
            chars = result["characteristics"]
            raw_feats = result["raw_features"]

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Result Status Banner
        col_res1, col_res2 = st.columns([1, 1])
        
        with col_res1:
            if is_phishing:
                st.markdown(f"""
                <div class="status-card-phishing">
                    <h3 style="color: #ef4444; margin:0;">🚨 POTENTIAL PHISHING</h3>
                    <p style="color: #fca5a5; margin: 0.4rem 0 0 0; font-size: 0.95rem;">
                        This website exhibits strong indicators of credential harvesting or fraudulent behavior.
                    </p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="status-card-legit">
                    <h3 style="color: #10b981; margin:0;">✅ LEGITIMATE WEBSITE</h3>
                    <p style="color: #a7f3d0; margin: 0.4rem 0 0 0; font-size: 0.95rem;">
                        Structural and security characteristics align with verified, legitimate web domains.
                    </p>
                </div>
                """, unsafe_allow_html=True)

        with col_res2:
            st.metric(
                label="Model Risk Score",
                value=f"{risk_score:.2f}%",
                delta=f"{risk_level} Risk Level",
                delta_color="inverse" if is_phishing else "normal"
            )
            st.progress(min(max(int(risk_score), 0), 100))

        st.markdown("---")

        # Granular Characteristics
        st.markdown("#### 📋 URL Characteristics Breakdown")
        col_c1, col_c2, col_c3, col_c4, col_c5 = st.columns(5)
        
        with col_c1:
            st.markdown(f"""
            <div class="char-metric-box">
                <small style="color:#9ca3af;">URL Length</small><br>
                <strong style="color:{'#ef4444' if chars['url_length'] == 'High' else '#10b981'}; font-size:1.1rem;">
                    {chars['url_length']} ({raw_feats.get('url_length', 0)})
                </strong>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
            <div class="char-metric-box">
                <small style="color:#9ca3af;">Special Chars</small><br>
                <strong style="color:{'#ef4444' if chars['special_characters'] == 'High' else '#10b981'}; font-size:1.1rem;">
                    {chars['special_characters']} ({raw_feats.get('num_special_chars', 0)})
                </strong>
            </div>
            """, unsafe_allow_html=True)

        with col_c3:
            st.markdown(f"""
            <div class="char-metric-box">
                <small style="color:#9ca3af;">Subdomains</small><br>
                <strong style="color:{'#ef4444' if chars['subdomains'] == 'High' else '#10b981'}; font-size:1.1rem;">
                    {chars['subdomains']} ({raw_feats.get('num_subdomains', 0)})
                </strong>
            </div>
            """, unsafe_allow_html=True)

        with col_c4:
            st.markdown(f"""
            <div class="char-metric-box">
                <small style="color:#9ca3af;">IP Address</small><br>
                <strong style="color:{'#ef4444' if chars['ip_address'] == 'Detected' else '#10b981'}; font-size:1.1rem;">
                    {chars['ip_address']}
                </strong>
            </div>
            """, unsafe_allow_html=True)

        with col_c5:
            st.markdown(f"""
            <div class="char-metric-box">
                <small style="color:#9ca3af;">HTTPS Security</small><br>
                <strong style="color:{'#10b981' if chars['https'] == 'Detected' else '#ef4444'}; font-size:1.1rem;">
                    {chars['https']}
                </strong>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Decision Explainability Section
        st.markdown("#### 💡 Decision Explainability & Risk Attribution")
        for exp in explanations:
            impact = exp["impact"]
            box_class = "reason-box-high" if impact == "High Risk" else ("reason-box-mod" if impact == "Moderate Risk" else "reason-box-safe")
            color_badge = "#ef4444" if impact == "High Risk" else ("#f59e0b" if impact == "Moderate Risk" else "#10b981")
            
            st.markdown(f"""
            <div class="{box_class}">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <strong style="color:#ffffff;">{exp['feature']}</strong>
                    <span style="background:rgba(255,255,255,0.1); color:{color_badge}; font-weight:700; font-size:0.8rem; padding:0.15rem 0.5rem; border-radius:4px;">
                        {impact}
                    </span>
                </div>
                <div style="color:#9ca3af; font-size:0.88rem; margin-top:0.25rem;">{exp['detail']}</div>
            </div>
            """, unsafe_allow_html=True)

        # Raw Extracted Features
        with st.expander("🛠️ View All 19 Extracted Feature Values"):
            feat_df = pd.DataFrame(list(raw_feats.items()), columns=["Feature Name", "Extracted Value"])
            st.dataframe(feat_df, use_container_width=True)


# =========================================================
# TAB 2: Model Evaluation & Visuals (PPT Artifacts)
# =========================================================
with tab_metrics:
    st.markdown("### 📊 Benchmark Evaluation & Presentation Figures")
    st.caption("Model evaluated on 12,000 unseen test records from the UCI PhiUSIIL Phishing URL Dataset.")

    # Load metrics CSV
    metrics_file = "results/metrics/model_comparison.csv"
    if os.path.exists(metrics_file):
        m_df = pd.read_csv(metrics_file)
        
        col_m1, col_m2, col_m3, col_m4, col_m5 = st.columns(5)
        scores = dict(zip(m_df["Metric"], m_df["Score"]))
        
        col_m1.metric("Accuracy", f"{scores.get('Accuracy', 0.9960)*100:.2f}%")
        col_m2.metric("Precision", f"{scores.get('Precision', 0.9944)*100:.2f}%")
        col_m3.metric("Recall", f"{scores.get('Recall', 0.9987)*100:.2f}%")
        col_m4.metric("F1-Score", f"{scores.get('F1-Score', 0.9965)*100:.2f}%")
        col_m5.metric("ROC-AUC", f"{scores.get('ROC-AUC', 0.9984):.4f}")

    st.markdown("---")

    col_fig1, col_fig2 = st.columns(2)
    with col_fig1:
        st.markdown("##### 📌 Confusion Matrix")
        cm_path = "results/figures/confusion_matrix.png"
        if os.path.exists(cm_path):
            st.image(cm_path, use_container_width=True, caption="Figure 1: Confusion Matrix on 12,000 Test Records")
        else:
            st.info("Run `python src/evaluate_model.py` to generate the confusion matrix figure.")

    with col_fig2:
        st.markdown("##### 📌 ROC Curve")
        roc_path = "results/figures/roc_curve.png"
        if os.path.exists(roc_path):
            st.image(roc_path, use_container_width=True, caption="Figure 2: Receiver Operating Characteristic (AUC = 0.9984)")
        else:
            st.info("Run `python src/evaluate_model.py` to generate the ROC curve figure.")

    st.markdown("---")
    st.markdown("##### 📌 XGBoost Top Feature Importances")
    fi_path = "results/figures/feature_importance.png"
    if os.path.exists(fi_path):
        st.image(fi_path, use_container_width=True, caption="Figure 3: Top URL Feature Importances Ranked by XGBoost")


# =========================================================
# TAB 3: Batch URL Analysis
# =========================================================
with tab_batch:
    st.markdown("### 🧪 Batch URL Scanner")
    st.caption("Scan multiple websites simultaneously by entering URLs below.")

    batch_input = st.text_area(
        "Enter URLs (one per line):",
        value="https://www.google.com\nhttp://192.168.1.1/update-account/bank-verify-secure\nhttps://www.github.com\nhttp://www.shprakserf.gq\nhttp://secure-paypal-login.account-verification-alert.com/signin",
        height=140
    )

    if st.button("⚡ Scan All URLs", type="primary"):
        urls = [u.strip() for u in batch_input.strip().split("\n") if u.strip()]
        if not urls:
            st.warning("Please provide at least one valid URL.")
        else:
            results_list = []
            progress_bar = st.progress(0)
            
            for idx, u in enumerate(urls):
                res = predictor.predict(u)
                results_list.append({
                    "URL": u,
                    "Prediction": res["prediction"],
                    "Risk Score": f"{res['risk_score']:.2f}%",
                    "Risk Level": res["risk_level"],
                    "HTTPS": res["characteristics"]["https"],
                    "IP Detected": res["characteristics"]["ip_address"],
                    "Subdomains": res["characteristics"]["subdomains"]
                })
                progress_bar.progress((idx + 1) / len(urls))

            batch_df = pd.DataFrame(results_list)
            st.dataframe(batch_df, use_container_width=True)

            # Download CSV option
            csv_data = batch_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Scan Results (CSV)",
                data=csv_data,
                file_name="phishing_batch_scan_results.csv",
                mime="text/csv"
            )
