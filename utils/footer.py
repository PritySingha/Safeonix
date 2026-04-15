# utils/footer.py
import streamlit as st
import base64
from pathlib import Path

def get_base64_of_image(image_path):
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        return ""

def show_footer():
    """Display a consistent footer with logo and credits."""
    logo_path = Path("static/safeonix_logo.png")
    logo_base64 = get_base64_of_image(logo_path)

    footer_html = f"""
    <style>
    .safeonix-footer {{
        margin-top: 68px;
        padding: 36px 0 22px;
        border-top: 1px solid rgba(255,255,255,0.06);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 20px;
        font-family: 'Inter', sans-serif;
    }}
    .footer-brand {{
        display: flex;
        align-items: center;
        gap: 12px;
    }}
    .footer-brand img {{
        height: 34px;
        width: auto;
        filter: drop-shadow(0 0 6px rgba(130,80,200,0.3));
    }}
    .footer-brand-text {{
        display: flex;
        flex-direction: column;
    }}
    .footer-brand-name {{
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #e8e0f8;
    }}
    .footer-brand-tagline {{
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 0.12em;
        color: #6b5a9e;
        text-transform: uppercase;
    }}
    .footer-copyright {{
        font-size: 12px;
        color: #363960;
    }}
    @media (max-width: 680px) {{
        .safeonix-footer {{
            flex-direction: column;
            text-align: center;
            justify-content: center;
        }}
        .footer-brand {{
            justify-content: center;
        }}
    }}
    </style>

    <div class="safeonix-footer">
        <div class="footer-brand">
            <img src="data:image/png;base64,{logo_base64}" alt="Safeonix Logo">
            <div class="footer-brand-text">
                <span class="footer-brand-name">SAFEONIX</span>
                <span class="footer-brand-tagline">AI Fraud Detection System</span>
            </div>
        </div>
        <div class="footer-copyright">
            © 2026 Safeonix – AI-powered fraud detection platform
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)