import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

from utils.storage import load_transactions
from utils.navbar import show_navbar
from utils.footer import show_footer

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Safeonix • Dashboard",
    page_icon="static/safeonix_logo.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# -------------------------------------------------
# LOAD CSS
# -------------------------------------------------
with open("assets/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -------------------------------------------------
# NAVBAR
# -------------------------------------------------
show_navbar(active_page="Dashboard")

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown("""
<div class="page-header">
Dashboard Overview
</div>
<div class="page-sub">
Live analytics of transaction behaviour and fraud detection results.
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------
# CACHED DATA LOADING (with safe conversion)
# -------------------------------------------------
@st.cache_data(ttl=60)
def get_transactions():
    df = load_transactions()
    if df.empty:
        return df
    
    # Ensure timestamp is datetime
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    
    # Safely convert is_fraud to int (handles string "True"/"False", bool, or numeric)
    if "is_fraud" in df.columns:
        # If column is object (string) or bool, map to int
        if df["is_fraud"].dtype in ["object", "bool"]:
            # Map common string representations
            mapping = {"True": 1, "False": 0, "true": 1, "false": 0, "1": 1, "0": 0}
            df["is_fraud"] = df["is_fraud"].astype(str).map(mapping).fillna(0).astype(int)
        else:
            # Already numeric, just convert to int
            df["is_fraud"] = df["is_fraud"].astype(int)
    return df

df = get_transactions()

# -------------------------------------------------
# EMPTY STATE
# -------------------------------------------------
if df.empty:
    st.markdown("""
    <div class="empty-state">
        🚫 No transaction data available.<br><br>
        Go to the <strong>Predict</strong> page and run some predictions first.<br>
        After that, come back here to see analytics and alerts.
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# -------------------------------------------------
# SIDEBAR FILTERS
# -------------------------------------------------
with st.sidebar:
    st.markdown("### 🔍 Filters")
    
    # Date range filter
    if "timestamp" in df.columns and not df["timestamp"].isnull().all():
        min_date = df["timestamp"].min().date()
        max_date = df["timestamp"].max().date()
        date_range = st.date_input(
            "Date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        if len(date_range) == 2:
            start_date, end_date = date_range
            mask = (df["timestamp"].dt.date >= start_date) & (df["timestamp"].dt.date <= end_date)
            df = df[mask].copy()
    
    # Transaction type filter
    if "type" in df.columns:
        types = ["All"] + sorted(df["type"].unique().tolist())
        selected_type = st.selectbox("Transaction type", types)
        if selected_type != "All":
            df = df[df["type"] == selected_type].copy()
    
        # Amount range filter
    if "amount" in df.columns:
        min_amt = float(df["amount"].min())
        max_amt = float(df["amount"].max())
        
        if min_amt == max_amt:
            st.info(f"📊 All transactions have the same amount: ${min_amt:,.2f}")
            # No slider – keep all data
        else:
            amount_range = st.slider(
                "Amount range",
                min_value=min_amt,
                max_value=max_amt,
                value=(min_amt, max_amt),
                step=100.0
            )
            df = df[(df["amount"] >= amount_range[0]) & (df["amount"] <= amount_range[1])]
    st.markdown("---")
    st.caption(f"Showing {len(df)} transactions")

# -------------------------------------------------
# KPI METRICS (Row 1)
# -------------------------------------------------
total = len(df)
if total == 0:
    st.warning("No transactions match the selected filters.")
    st.stop()

fraud = int(df["is_fraud"].sum())
safe = total - fraud
fraud_rate = (fraud / total) * 100 if total > 0 else 0

total_amount = df["amount"].sum()
fraud_amount = df[df["is_fraud"] == 1]["amount"].sum() if fraud > 0 else 0

metrics_html = f"""
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-label">📊 Total Transactions</div>
        <div class="metric-value">{total:,}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">⚠️ Fraudulent</div>
        <div class="metric-value">{fraud:,}</div>
        <div class="metric-delta negative">{fraud_rate:.1f}%</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">✅ Safe</div>
        <div class="metric-value">{safe:,}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">💰 Total Volume</div>
        <div class="metric-value">${total_amount:,.0f}</div>
    </div>
    <div class="metric-card">
        <div class="metric-label">💸 Fraud Volume</div>
        <div class="metric-value">${fraud_amount:,.0f}</div>
    </div>
</div>
"""
st.markdown(metrics_html, unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# CHARTS (Row 2)
# -------------------------------------------------
row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    fig_pie = go.Figure(data=[go.Pie(
        labels=["Safe", "Fraud"],
        values=[safe, fraud],
        hole=0.6,
        marker=dict(colors=["#22c886", "#ef6060"]),
        textinfo="percent+label",
        textfont=dict(color="white")
    )])
    fig_pie.update_layout(
        title="Safe vs Fraud Transactions",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        height=400,
        margin=dict(t=40, b=0)
    )
    st.plotly_chart(fig_pie, use_container_width=True)

with row2_col2:
    if "type" in df.columns:
        fraud_by_type = df.groupby("type")["is_fraud"].sum().reset_index()
        fraud_by_type.columns = ["Transaction Type", "Fraud Count"]
        fig_bar = px.bar(
            fraud_by_type,
            x="Transaction Type",
            y="Fraud Count",
            color="Fraud Count",
            color_continuous_scale="reds",
            title="Fraud Count by Transaction Type"
        )
        fig_bar.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            height=400,
            xaxis=dict(tickangle=0)
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Column 'type' not available. Cannot show breakdown by transaction type.")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------
# RECENT TRANSACTIONS TABLE (Last 5, compact)
# -------------------------------------------------
st.subheader("📋 Recent Transactions (Last 5)")

if "timestamp" in df.columns:
    df_recent = df.sort_values("timestamp", ascending=False).head(5)
else:
    df_recent = df.tail(5)

display_cols = ["amount", "type", "is_fraud"]
if "timestamp" in df.columns:
    display_cols = ["timestamp"] + display_cols
for col in ["nameOrig", "nameDest", "oldbalanceOrg", "newbalanceOrig"]:
    if col in df.columns:
        display_cols.append(col)

df_display = df_recent[display_cols].copy()
df_display["Risk"] = df_display["is_fraud"].map({0: "✅ Safe", 1: "⚠️ Fraud"})
df_display["amount"] = df_display["amount"].apply(lambda x: f"${x:,.2f}")
df_display = df_display.drop(columns=["is_fraud"])

st.markdown("""
<style>
.compact-dataframe {
    font-size: 12px;
}
.compact-dataframe td, .compact-dataframe th {
    padding: 4px 8px !important;
}
.fraud-row {
    background-color: rgba(239, 96, 96, 0.15) !important;
}
</style>
""", unsafe_allow_html=True)

def highlight_fraud(row):
    if row["Risk"] == "⚠️ Fraud":
        return ["background-color: rgba(239, 96, 96, 0.2)"] * len(row)
    else:
        return [""] * len(row)

styled_df = df_display.style.apply(highlight_fraud, axis=1)
st.dataframe(styled_df, use_container_width=True, height=215, hide_index=True)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
show_footer()