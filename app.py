import streamlit as st
from utils.navbar import show_navbar
from utils.footer import show_footer
# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(
    page_title="Safeonix",
    page_icon="static/safeonix_logo.png",
    layout="wide"
)

# ---------------------------------
# LOAD CSS
# ---------------------------------
with open("assets/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------
# NAVBAR
# ---------------------------------
show_navbar("Home")

# ---------------------------------
# HERO TOP BADGE
# ---------------------------------
st.markdown("""
<div class="eyebrow">
    <div class="eyebrow-dot"></div>
    <span>Trusted AI Fraud Detection</span>
</div>
""", unsafe_allow_html=True)

# ---------------------------------
# HERO SECTION (fixed side-by-side)
# ---------------------------------
hero_html = """
<div class="hero-layout">
    <div>
        <h1 style="font-size:50px; font-weight:700; line-height:1.06; letter-spacing:-0.03em; margin-bottom:20px;">
            Protect transactions.<br>
            <em style="font-style:normal; background:linear-gradient(135deg,#a878f0,#7040c0); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;">
                Detect fraud
            </em><br>
            instantly.
        </h1>
        <p class="hero-sub">
            Safeonix identifies suspicious financial activity in real time using
            machine learning trained on transactional patterns and fraud signals.
        </p>
        <div class="hero-actions">
            <a href="/Predict" target="_self" class="btn-main">Try Prediction →</a>
            <a href="/Dashboard" target="_self" class="btn-light">View Dashboard</a>
        </div>
    </div>
    <div class="hero-card">
        <div class="hero-card-title">Recent Predictions</div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">TXN #8821</div>
                <div class="mini-stat-type">₹4,200 · TRANSFER</div>
            </div>
            <span class="risk-badge risk-safe">Safe</span>
        </div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">TXN #8820</div>
                <div class="mini-stat-type">₹18,500 · CASH_OUT</div>
            </div>
            <span class="risk-badge risk-high">High Risk</span>
        </div>
        <div class="mini-stat">
            <div>
                <div class="mini-stat-label">TXN #8819</div>
                <div class="mini-stat-type">₹940 · PAYMENT</div>
            </div>
            <span class="risk-badge risk-med">Medium</span>
        </div>
        <div class="live-bar">
            <span class="live-bar-ts">Last updated 2m ago</span>
            <span class="live-pill">
                <span class="live-dot"></span>
                Live
            </span>
        </div>
    </div>
</div>
"""

st.markdown(hero_html, unsafe_allow_html=True)

# ---------------------------------
# TRUST STRIP
# ---------------------------------
st.markdown("""
<div class="trust-strip">

<div class="trust-item">99.2% Accuracy</div>
<div class="trust-item">Realtime Decisions</div>
<div class="trust-item">6M+ Records Analyzed</div>
<div class="trust-item">XGBoost Powered</div>

</div>
""", unsafe_allow_html=True)

# ---------------------------------
# SECTION DIVIDER
# ---------------------------------
st.markdown("""
<div style="
border-top:1px solid rgba(255,255,255,0.06);
margin:68px 0 0;
padding-top:48px;
"></div>
""", unsafe_allow_html=True)

# ---------------------------------
# FEATURES HEADER
# ---------------------------------
st.markdown("""
<div class="section-label">Capabilities</div>

<h2 style="
font-size:29px;
font-weight:700;
letter-spacing:-0.02em;
margin-bottom:10px;
">
What Safeonix offers
</h2>

<p class="section-desc">
Fast, explainable, and production-ready fraud detection built for modern finance teams.
</p>
""", unsafe_allow_html=True)

# ---------------------------------
# FEATURES GRID
# ---------------------------------
features = """
<div class="grid-3">

<div class="card-clean featured">
<h3>Instant Analysis</h3>
<p>
Evaluate suspicious transactions in seconds.
The model processes balances, amount, and type
to produce a risk label instantly.
</p>

<div class="response-box">
<div class="response-box-label">Avg response time</div>
<div class="response-big">~40<span class="response-unit">ms</span></div>
</div>
</div>

<div class="card-clean">
<h3>Live Dashboard</h3>
<p>Track fraud metrics and transaction behavior across sessions.</p>
</div>

<div class="card-clean">
<h3>Email Alerts</h3>
<p>Immediate notifications on high-risk transaction activity.</p>
</div>

<div class="card-clean">
<h3>Risk Labels</h3>
<p>Safe, Medium Risk, and High Risk for every prediction.</p>
</div>

<div class="card-clean">
<h3>Audit Logs</h3>
<p>Full prediction history and decision records maintained automatically.</p>
</div>

</div>
"""
st.markdown(features, unsafe_allow_html=True)

# ---------------------------------
# PERFORMANCE DIVIDER
# ---------------------------------
st.markdown("""
<div style="
border-top:1px solid rgba(255,255,255,0.06);
margin:68px 0 0;
padding-top:48px;
"></div>
""", unsafe_allow_html=True)

# ---------------------------------
# PERFORMANCE HEADER
# ---------------------------------
st.markdown("""
<div class="section-label">Model Performance</div>

<h2 style="
font-size:29px;
font-weight:700;
letter-spacing:-0.02em;
margin-bottom:10px;
">
Numbers that matter
</h2>

<p class="section-desc">
Trained on 6M+ real-world transactions with rigorous cross-validation.
</p>
""", unsafe_allow_html=True)

# ---------------------------------
# STATS
# ---------------------------------
stats = """
<div class="stats-row">

<div class="stat-box featured">
<div class="big">99.2<span style="font-size:22px;color:#a878f0">%</span></div>
<div class="stat-unit">Overall Accuracy</div>
<div class="stat-sub">Validated on held-out test set</div>
</div>

<div class="stat-box">
<div class="big">98.1%</div>
<div class="stat-unit">Precision</div>
</div>

<div class="stat-box">
<div class="big">81.4%</div>
<div class="stat-unit">Recall</div>
</div>

<div class="stat-box">
<div class="big">88.2%</div>
<div class="stat-unit">F1-score</div>
</div>

</div>
"""
st.markdown(stats, unsafe_allow_html=True)

# ---------------------------------
# FOOTER
# ---------------------------------
show_footer()