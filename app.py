import streamlit as st
import plotly.graph_objects as go

# ---------- הגדרות דף ----------
st.set_page_config(page_title="The Authenticity Auditor", page_icon="🛡️", layout="centered")

# ---------- עיצוב דחוס עם ניגודיות מקסימלית ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700;800&display=swap');
    
    /* הגדרות בסיס - דחיסות שורות */
    html, body, [class*="st-"] { 
        direction: RTL; 
        text-align: right; 
        font-family: 'Assistant', sans-serif; 
        line-height: 1.2 !important; 
    }
    
    .stApp { background-color: #000000; }

    /* כותרות ענק */
    h1 {
        color: #00FFCC !important;
        font-size: 3.5rem !important;
        font-weight: 800 !important;
        margin-bottom: 0.5rem !important;
        padding-top: 0rem !important;
    }
    h3 {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin-top: -1rem !important;
        margin-bottom: 1rem !important;
    }
    h4 {
        color: #00FFCC !important;
        font-size: 1.4rem !important;
        margin-bottom: 0.5rem !important;
    }

    /* טקסט לבן בוהק ודחוס */
    p, span, label, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 700 !important;
        font-size: 1.1rem !important;
    }

    /* צמצום רווחים בין אלמנטים של Streamlit */
    .stVerticalBlock {
        gap: 0.5rem !important;
    }

    /* עיצוב צ'קבוקסים דחוסים */
    .stCheckbox {
        margin-bottom: -0.8rem !important;
    }
    .stCheckbox label {
        background-color: #111111;
        padding: 5px 12px !important;
        border-radius: 5px;
        border: 1px solid #333;
    }

    /* תיבות קלט */
    .stNumberInput {
        margin-bottom: -1rem !important;
    }

    /* כפתור דומיננטי */
    .stButton button {
        width: 100%;
        background-color: #00FFCC !important;
        color: #000000 !important;
        font-weight: 800 !important;
        font-size: 1.5rem !important;
        border-radius: 5px !important;
        margin-top: 1
