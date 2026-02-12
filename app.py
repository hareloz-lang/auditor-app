import streamlit as st
import plotly.graph_objects as go
import urllib.parse

# ---------- הגדרות דף ----------
st.set_page_config(page_title="THE AUDITOR", page_icon="🛡️", layout="centered")

# ---------- CSS ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@800;900&display=swap');
    html, body, [class*="st-"] { direction: rtl !important; text-align: right !important; font-family: 'Assistant', sans-serif; }
    .stApp { background-color: #000000; }
    .main-title { color: #00FFCC !important; font-size: clamp(3rem, 10vw, 6rem) !important; font-weight: 900 !important; line-height: 0.8 !important; margin-bottom: 5px !important; letter-spacing: -2px; }
    .sub-title { color: #FFFFFF !important; font-size: 1.6rem !important; font-weight: 800 !important; margin-bottom: 20px !important; }
    h4 { color: #00FFCC !important; font-size: 1.8rem !important; font-weight: 900 !important; border-bottom: 4px solid #00FFCC; display: inline-block; margin-bottom: 15px !important; }
    [data-testid="stCheckbox"] label { display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 10px !important; background: #111; margin-bottom: 5px; border-radius: 4px; }
    p, span, label, .stMarkdown { color: #FFFFFF !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    input { background-color: #111 !important; color: #00FFCC !important; font-size: 1.2rem !important; border: 2px solid #333 !important; text-align: right !important; }
    .stButton button { width: 100%; background-color: #00FFCC !important; color: #000 !important; font-size: 2rem !important; font-weight: 900 !important; height: 60px !important; border-radius: 0px !important; border: none !important; margin-top: 10px; }
    .whatsapp-button { display: block; background-color: #25D366; color: white !important; padding: 12px; text-decoration: none; font-size: 1.3rem; font-weight: 900; border-radius: 5px; text-align: center; width: 100%; margin-top: 10px; }
    
    .insight-box {
        border: 2px solid #00FFCC;
        background-color: rgba(0, 255, 204, 0.05);
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
        color: #FFFFFF;
        font-weight: 800;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
        st.session_state.final_score = 0
        st.session_state.insight = ""

    st.markdown('<div class="main-title">AUDITOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">מערכת אימות אמינות משתמשים</div>', unsafe_allow_html=True)

    st.text_input("🔗 לינק לסרטון", placeholder="ה
