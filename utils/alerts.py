import smtplib
import streamlit as st
from email.message import EmailMessage

def send_fraud_alert(recipient_email, transaction_data, fraud_probability):
    try:
        password = st.secrets["GMAIL_APP_PASSWORD"]
        sender = st.secrets["GMAIL_SENDER_EMAIL"]
    except KeyError as e:
        st.error(f"Missing secret: {e}")
        return False

    subject = f"🚨 FRAUD ALERT: High-Risk Transaction Detected"
    body = f"""
    A high-risk transaction was detected by your Safeonix fraud detection system.

    Transaction Details:
    - Amount: ${transaction_data['amount']:,.2f}
    - Type: {transaction_data['type']}
    - Fraud Probability: {fraud_probability:.2%}

    Please log in to your Safeonix Dashboard for more details.
    """
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)
        st.success("📧 Alert email sent successfully.")
        return True
    except Exception as e:
        st.error(f"❌ Failed to send email: {e}")
        return False