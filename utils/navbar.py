# utils/navbar.py
import streamlit as st
import base64
from pathlib import Path

def get_base64_of_image(image_path):
    """Convert image file to base64 string for embedding in HTML."""
    try:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except FileNotFoundError:
        # Fallback: return empty string (will show placeholder)
        return ""

def show_navbar(active_page="Home"):
    """
    Display a sticky, responsive top navbar with logo.
    active_page: "Home", "Dashboard", "Predict" - highlights the active link.
    """
    # Path to your logo (adjust if your logo is elsewhere)
    logo_path = Path("static/safeonix_logo.png")
    logo_base64 = get_base64_of_image(logo_path)

    # Build the navbar HTML with inline CSS for stickiness + responsiveness
    navbar_html = f"""
    <style>
    /* ----- STICKY NAVBAR ----- */
    .safeonix-nav {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(12, 11, 20, 0.92);
        backdrop-filter: blur(12px);
        border-bottom: 1px solid rgba(255,255,255,0.06);
        z-index: 1000;
        padding: 0.75rem 2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        font-family: 'Inter', sans-serif;
        box-sizing: border-box;
    }}
    .nav-brand {{
        display: flex;
        align-items: center;
        gap: 10px;
        text-decoration: none;
    }}
    .nav-brand img {{
        height: 36px;
        width: auto;
        filter: drop-shadow(0 0 6px rgba(130,80,200,0.4));
    }}
    .brand-text {{
        display: flex;
        flex-direction: column;
        line-height: 1.2;
    }}
    .brand-name {{
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.1em;
        color: #e8e0f8;
    }}
    .brand-tagline {{
        font-size: 9px;
        font-weight: 500;
        letter-spacing: 0.12em;
        color: #6b5a9e;
        text-transform: uppercase;
    }}
    .nav-links {{
        display: flex;
        gap: 0.25rem;
        flex-wrap: wrap;
    }}
    .nav-links a {{
        text-decoration: none;
        color: #7a80a0;
        font-size: 13.5px;
        font-weight: 500;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        transition: 0.2s ease;
    }}
    .nav-links a:hover {{
        background: rgba(130,80,200,0.1);
        color: #e0daf5;
    }}
    .nav-links a.active {{
        background: rgba(130,80,200,0.2);
        color: #c4b5f7;
    }}
    /* ----- RESPONSIVE (mobile) ----- */
    @media (max-width: 680px) {{
        .safeonix-nav {{
            padding: 0.6rem 1rem;
            flex-direction: column;
            gap: 0.6rem;
        }}
        .nav-links a {{
            padding: 0.4rem 0.8rem;
            font-size: 12px;
        }}
        .brand-name {{
            font-size: 12px;
        }}
    }}
    /* Push main content down so it's not hidden behind fixed navbar */
    .main-content-padding {{
        margin-top: 80px;
    }}
    </style>

    <div class="safeonix-nav">
        <div class="nav-brand">
            <img src="data:image/png;base64,{logo_base64}" alt="Safeonix Logo">
            <div class="brand-text">
                <span class="brand-name">SAFEONIX</span>
                <span class="brand-tagline">AI Fraud Detection</span>
            </div>
        </div>
        <div class="nav-links">
            <a href="/" target="_self" class="{'active' if active_page == 'Home' else ''}">🏠 Home</a>
            <a href="/Dashboard" target="_self" class="{'active' if active_page == 'Dashboard' else ''}">📊 Dashboard</a>
            <a href="/Predict" target="_self" class="{'active' if active_page == 'Predict' else ''}">🛡️ Predict</a>
        </div>
    </div>
    <div class="main-content-padding"></div>
    """

    st.markdown(navbar_html, unsafe_allow_html=True)

    # Hide Streamlit's default header and sidebar completely
    st.markdown("""
    <style>
        header[data-testid="stHeader"] {display: none;}
        [data-testid="stSidebar"] {display: none;}
    </style>
    """, unsafe_allow_html=True)