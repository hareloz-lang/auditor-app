import streamlit as st
import plotly.graph_objects as go

# ---------- הגדרות דף ----------
st.set_page_config(page_title="The Authenticity Auditor", page_icon="🛡️", layout="centered")

# ---------- עיצוב משופר עם ניגודיות גבוהה ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700;800&display=swap');
    
    /* הגדרות כלליות */
    html, body, [class*="st-"] { 
        direction: RTL; 
        text-align: right; 
        font-family: 'Assistant', sans-serif; 
    }
    
    /* רקע וצבע טקסט ראשי */
    .stApp { 
        background-color: #000000; 
    }
    
    /* טקסט לבן בוהק לכל האפליקציה */
    p, span, label, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
    }

    /* כותרות בולטות */
    h1, h2, h3 {
        color: #00FFCC !important; /* צבע טורקיז ניאון */
        font-weight: 800 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
    }

    /* עיצוב תיבות הקלט */
    .stNumberInput input {
        background-color: #1e1e1e !important;
        color: #FFFFFF !important;
        border: 1px solid #00FFCC !important;
    }

    /* עיצוב הצ'קבוקסים */
    .stCheckbox label {
        background-color: #1a1a1a;
        padding: 10px 15px;
        border-radius: 8px;
        border: 1px solid #333;
        display: block;
        transition: 0.3s;
    }
    .stCheckbox label:hover {
        border-color: #00FFCC;
    }

    /* כפתור הניתוח */
    .stButton button {
        width: 100%;
        background-color: #00FFCC !important;
        color: #000000 !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        border-radius: 10px !important;
        height: 3em !important;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🛡️ The Authenticity Auditor")
    st.markdown("### כלי הניתוח המקצועי לאמינות ברשת")

    # --- נתונים יבשים ---
    st.write("---")
    st.markdown("#### 📊 שלב א': בדיקת מעורבות (Engagement)")
    
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("כמות עוקבים כוללת", min_value=0, value=1000, step=100)
    with col2:
        likes = st.number_input("ממוצע לייקים לסרטון", min_value=0, value=10, step=10)
    
    er = (likes / followers) * 100 if followers > 0 else 0
    
    # תצוגת ER בולטת
    if er < 1 and followers > 2000:
        st.error(f"אחוז מעורבות נמוך מאוד: {er:.2f}% (חשד לעוקבים קנויים)")
    else:
        st.info(f"אחוז מעורבות: {er:.2f}%")

    # --- שאלון אדום ---
    st.write("---")
    st.markdown("#### 🚩 שלב ב': זיהוי דפוסי הונאה")
    
    q1 = st.checkbox("הבטחה לרווח מהיר / 'כסף בזמן שינה' / 'שיטה סודית'")
    q2 = st.checkbox("מצג שווא של עושר (רכבי יוקרה מושכרים, ערימות מזומנים)")
    q3 = st.checkbox("לחץ זמן מניפולטיבי ('נותרו 2 מקומות', 'הזדמנות של פעם בחיים')")
    q4 = st.checkbox("חוסר בשקיפות (אין אתר רשמי, אין שם חברה, אין פנים מאחורי העסק)")
    q5 = st.checkbox("הפניה לערוץ טלגרם סגור או לשיחת וואטסאפ אישית בלבד")
    q6 = st.checkbox("תגובות חסומות או תגובות שנראות כמו בוטים גנריים")

    # לוגיקת חישוב
    score = 0
    if er < 1 and followers > 5000: score += 30
    if q1: score += 25
    if q2: score += 15
    if q3: score += 15
    if q4: score += 20
    if q5: score += 15
    if q6: score += 10
    
    final_score = min(score, 100)

    st.write("---")
    if st.button("הפעל ניתוח סיכון"):
        # מד Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            number = {'font': {'color': "#FFFFFF", 'size': 50}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF"},
                'bar': {'color': "#FF4B4B" if final_score > 50 else "#FFA500" if final_score > 20 else "#00FFCC"},
                'bgcolor': "#1e1e1e",
                'steps': [
                    {'range': [0, 25], 'color': "#004d40"},
                    {'range': [25, 60], 'color': "#4d3a00"},
                    {'range': [60, 100], 'color': "#4d0000"}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("🛑 רמת סיכון גבוהה! יש כאן הצטברות משמעותית של סימני הונאה.")
        elif final_score > 25:
            st.warning("⚠️ זהירות. ישנם מספר 'דגלים אדומים'. מומלץ לבדוק ביקורות חיצוניות.")
        else:
            st.success("💎 נראה תקין. לא נמצאו דפוסים קלאסיים של הונאה.")

if __name__ == "__main__":
    main()
