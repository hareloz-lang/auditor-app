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
        margin-top: 1rem !important;
    }
    
    /* הסתרת רווחים מיותרים למעלה */
    .block-container {
        padding-top: 2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🛡️ AUDITOR")
    st.subheader("ניתוח אמינות בזמן אמת")

    # --- שלב א' ---
    st.markdown("#### 📊 מעורבות (Engagement)")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים", min_value=0, value=1000)
    with col2:
        likes = st.number_input("לייקים", min_value=0, value=10)
    
    er = (likes / followers) * 100 if followers > 0 else 0
    st.write(f"ER: **{er:.2f}%**")

    # --- שלב ב' ---
    st.write("")
    st.markdown("#### 🚩 סימנים מחשידים (Red Flags)")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'סודות'")
    q2 = st.checkbox("מצג שווא של עושר (רכבים/מזומן)")
    q3 = st.checkbox("לחץ זמן מניפולטיבי")
    q4 = st.checkbox("חוסר בשקיפות / אין פנים")
    q5 = st.checkbox("הפניה לטלגרם/וואטסאפ בלבד")
    q6 = st.checkbox("תגובות חסומות או בוטים")

    # חישוב
    score = 0
    if er < 1 and followers > 5000: score += 30
    if q1: score += 25
    if q2: score += 15
    if q3: score += 15
    if q4: score += 20
    if q5: score += 15
    if q6: score += 10
    final_score = min(score, 100)

    if st.button("הרץ בדיקה"):
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            number = {'font': {'color': "#FFFFFF"}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF"},
                'bar': {'color': "#FF4B4B" if final_score > 50 else "#00FFCC"},
                'bgcolor': "#222222",
                'steps': [
                    {'range': [0, 50], 'color': "#004433"},
                    {'range': [50, 100], 'color': "#440000"}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("🛑 רמת סיכון גבוהה!")
        elif final_score > 25:
            st.warning("⚠️ דגלים אדומים זוהו.")
        else:
            st.success("💎 נראה תקין.")

if __name__ == "__main__":
    main()
