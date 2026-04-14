import streamlit as st
from utils.predict import predict_fraud
from utils.storage import save_transaction
from utils.alerts import send_fraud_alert
from utils.navbar import show_navbar
from utils.footer import show_footer

# -----------------------------------
# PAGE CONFIG
# -----------------------------------
st.set_page_config(
    page_title="Safeonix • Predict",
    page_icon="static/safeonix_logo.png",
    layout="wide"
)

# -----------------------------------
# LOAD CSS
# -----------------------------------
with open("assets/styles.css", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# -----------------------------------
# NAVBAR
# -----------------------------------
show_navbar(active_page="Predict")

# -----------------------------------
# INITIALIZE SESSION STATE (keep form values)
# -----------------------------------
defaults = {
    "txn_type": "CASH_OUT",
    "amount": 5000.0,
    "old_org": 10000.0,
    "new_org": 5000.0,
    "old_dest": 0.0,
    "new_dest": 5000.0,
    "email": ""
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# -----------------------------------
# RESPONSIVE LAYOUT (using CSS grid)
# -----------------------------------
st.markdown("""
<style>
@media (max-width: 768px) {
    .predict-grid {
        grid-template-columns: 1fr !important;
        gap: 1.5rem;
    }
}
.predict-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
    margin-top: 1rem;
}
.input-card, .result-card {
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1.5rem;
}
.input-card h3 {
    margin-top: 0;
    margin-bottom: 1.2rem;
    font-size: 1.2rem;
}
.result-card {
    background: rgba(120,64,200,0.03);
    border-color: rgba(120,64,200,0.2);
}
.risk-badge-large {
    display: inline-block;
    padding: 0.3rem 1rem;
    border-radius: 40px;
    font-weight: 700;
    font-size: 1rem;
    margin-bottom: 1rem;
}
.prob-bar {
    background: rgba(255,255,255,0.1);
    border-radius: 20px;
    height: 10px;
    overflow: hidden;
    margin: 1rem 0;
}
.prob-fill {
    height: 100%;
    border-radius: 20px;
    transition: width 0.3s;
}
.help-text {
    font-size: 11px;
    color: #7a80a0;
    margin-top: 4px;
}
.center-button {
    display: flex;
    justify-content: center;
    margin: 1.5rem 0 0.5rem;
}
</style>
<div>
    <div>
        <h3>📝 Transaction Details</h3>
""", unsafe_allow_html=True)

# -----------------------------------
# LEFT COLUMN: INPUT FORM
# -----------------------------------

# Transaction type
st.selectbox(
    "Transaction Type",
    ["CASH_OUT", "TRANSFER", "PAYMENT", "CASH_IN", "DEBIT"],
    index=["CASH_OUT", "TRANSFER", "PAYMENT", "CASH_IN", "DEBIT"].index(st.session_state.txn_type),
    key="txn_type"
)

# Amount
st.number_input("Amount (₹)", min_value=0.0, value=st.session_state.amount, step=100.0, key="amount")

# Sender balances
st.markdown("#### Sender Account")
col_a, col_b = st.columns(2)
with col_a:
    st.number_input("Old Balance", min_value=0.0, value=st.session_state.old_org, step=100.0, key="old_org")
with col_b:
    st.number_input("New Balance", min_value=0.0, value=st.session_state.new_org, step=100.0, key="new_org")

# Receiver balances
st.markdown("#### Receiver Account")
col_c, col_d = st.columns(2)
with col_c:
    st.number_input("Old Balance", min_value=0.0, value=st.session_state.old_dest, step=100.0, key="old_dest")
with col_d:
    st.number_input("New Balance", min_value=0.0, value=st.session_state.new_dest, step=100.0, key="new_dest")

# Email (optional)
st.text_input("Alert Email (optional)", key="email")
st.markdown('<div class="help-text">🔔 Receive an email alert if fraud is detected.</div>', unsafe_allow_html=True)

# Centered Analyze button using columns
col_btn_left, col_btn_center, col_btn_right = st.columns([1, 2, 1])
with col_btn_center:
    analyze_clicked = st.button("🔍 Analyze Transaction", use_container_width=True, type="primary")
    
# -----------------------------------
# RIGHT COLUMN: RESULT CARD
# -----------------------------------
st.markdown('<div class="result-card">', unsafe_allow_html=True)
st.markdown("<h3>📊 Analysis Result</h3>", unsafe_allow_html=True)

if analyze_clicked:
    # --- Input Validation ---
    errors = []
    if st.session_state.new_org > st.session_state.old_org:
        errors.append("Sender's new balance cannot be greater than old balance.")
    if st.session_state.new_dest > st.session_state.old_dest and st.session_state.old_dest > 0:
        errors.append("Receiver's new balance cannot exceed old balance (unless old balance is zero).")
    if st.session_state.amount <= 0:
        errors.append("Amount must be greater than zero.")

    if errors:
        for err in errors:
            st.error(err)
        st.stop()

    # Prepare input dict
    input_data = {
        "type": st.session_state.txn_type,
        "amount": st.session_state.amount,
        "oldbalanceOrg": st.session_state.old_org,
        "newbalanceOrig": st.session_state.new_org,
        "oldbalanceDest": st.session_state.old_dest,
        "newbalanceDest": st.session_state.new_dest
    }

    with st.spinner("🧠 Running fraud analysis..."):
        try:
            result = predict_fraud(input_data)
            prob = result["probability"]
            label = result["label"]
            is_fraud = result["is_fraud"]

            # Determine color and badge
            if label == "SAFE":
                badge_color = "#22c886"
                badge_text = "✅ SAFE"
                prob_color = "#22c886"
            elif label == "MEDIUM RISK":
                badge_color = "#f0a020"
                badge_text = "⚠️ MEDIUM RISK"
                prob_color = "#f0a020"
            else:
                badge_color = "#ef6060"
                badge_text = "🔴 HIGH RISK"
                prob_color = "#ef6060"

            # Show result card content
            st.markdown(f"""
            <div class="risk-badge-large" style="background:{badge_color}20; color:{badge_color}; border:1px solid {badge_color}40;">
                {badge_text}
            </div>
            <div style="font-size: 2rem; font-weight: 700;">{prob:.1%}</div>
            <div style="font-size: 0.85rem; color:#aaa;">Fraud Probability</div>
            <div class="prob-bar">
                <div class="prob-fill" style="width:{prob*100}%; background:{prob_color};"></div>
            </div>
            """, unsafe_allow_html=True)

            # Additional metrics
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Transaction Amount", f"₹{input_data['amount']:,.2f}")
            col_m2.metric("Type", input_data['type'])

            # Save to history
            save_transaction({
                **input_data,
                "probability": prob,
                "label": label,
                "is_fraud": int(is_fraud)
            })

            # Send email alert if transaction is fraudulent and an email is provided
            if is_fraud and st.session_state.email:
                with st.spinner("Sending alert email..."):
                    sent = send_fraud_alert(st.session_state.email, input_data, prob)
                    
            # Expandable raw input
            with st.expander("📄 View raw input data"):
                st.json(input_data)

        except Exception as e:
            st.error(f"Prediction failed: {str(e)}")
            st.info("Please check that the fraud model is loaded correctly.")
else:
    st.markdown("""
    <div class="empty-state" style="text-align:center; padding: 2rem;">
        ✨ Enter transaction details and click <strong>Analyze Transaction</strong> to see the risk assessment.
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # close result-card
st.markdown("</div>", unsafe_allow_html=True)  # close predict-grid

# -----------------------------------
# FOOTER
# -----------------------------------
show_footer()