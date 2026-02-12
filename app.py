import streamlit as st
import plotly.graph_objects as go

# ---------- הגדרות דף ----------
st.set_page_config(page_title="The Authenticity Auditor", page_icon="🛡️", layout="centered")

# ---------- עיצוב מתקדם ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="st-"] { direction: RTL; text-align: right; font-family: 'Assistant', sans-serif; }
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stRadio > label { font-size: 1.2rem !important; font-weight: bold; color: #00ffcc !important; }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("🛡️ The Authenticity Auditor")
    st.subheader("גרסה 1.1 - זיהוי הונאות והבטחות שווא")

    # --- נתונים יבשים ---
    with st.expander("📊 שלב א': נתוני חשבון (Engagement)", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            followers = st.number_input("כמות עוקבים", min_value=0, value=1000)
        with col2:
            likes = st.number_input("ממוצע לייקים לסרטון", min_value=0, value=10)
        
        er = (likes / followers) * 100 if followers > 0 else 0
        st.info(f"אחוז מעורבות (ER): {er:.2f}%")

    # --- שאלון אדום ---
    st.write("### 🚩 שלב ב': סימנים אדומים (Red Flags)")
    
    q1 = st.checkbox("הבטחה לרווח מהיר / 'כסף בזמן שינה'")
    q2 = st.checkbox("הצגת עושר מוגזם (מכוניות יוקרה, ערימות מזומנים, דובאי)")
    q3 = st.checkbox("לחץ זמן מסיבי ('רק ל-24 שעות הקרובות', 'מקומות אחרונים')")
    q4 = st.checkbox("חוסר שקיפות: אין שם חברה רשום או כתובת משרדים")
    q5 = st.checkbox("הפניה לוואטסאפ/טלגרם במקום אתר סליקה רשמי")
    q6 = st.checkbox("תגובות בסרטון נראות גנריות ('מדהים!', 'שינית לי את החיים')")

    # חישוב ציון
    score = 0
    if er < 1 and followers > 5000: score += 30  # חשד לעוקבים קנויים
    if q1: score += 25
    if q2: score += 15
    if q3: score += 15
    if q4: score += 20
    if q5: score += 15
    if q6: score += 10
    
    final_score = min(score, 100)

    if st.button("בצע ניתוח סופי"):
        st.write("---")
        # מד Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "red" if final_score > 50 else "orange" if final_score > 20 else "green"},
                'steps': [{'range': [0, 25], 'color': "lightgreen"}, {'range': [25, 60], 'color': "yellow"}, {'range': [60, 100], 'color': "red"}]
            }
        ))
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("❌ רמת סיכון גבוהה מאוד. רוב הסיכויים שמדובר בהונאה או שיווק אגרסיבי מדי.")
        elif final_score > 25:
            st.warning("⚠️ יש להיזהר. נתגלו מספר סימנים מחשידים. מומלץ לבצע בדיקת רקע בגוגל.")
        else:
            st.success("✅ נראה אמין יחסית. תמיד כדאי להפעיל שיקול דעת.")

if __name__ == "__main__":
    main()
