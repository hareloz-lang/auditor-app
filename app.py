import streamlit as st
import plotly.graph_objects as go

# ---------- הגדרות דף ----------
st.set_page_config(page_title="THE AUDITOR", page_icon="🛡️", layout="centered")

# ---------- CSS אגרסיבי לתיקון הצ'קבוקסים והוספת לינק ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@800;900&display=swap');
    
    /* הגדרות בסיס ויישור לימין */
    html, body, [class*="st-"], .main-title, .sub-title { 
        direction: RTL !important; 
        text-align: right !important; 
        font-family: 'Assistant', sans-serif; 
    }
    
    .stApp { background-color: #000000; }
    
    /* כותרות */
    .main-title {
        color: #00FFCC !important;
        font-size: 6rem !important;
        font-weight: 900 !important;
        line-height: 0.8 !important;
        margin-bottom: 5px !important;
        letter-spacing: -2px;
        display: block;
        width: 100%;
    }
    
    .sub-title {
        color: #FFFFFF !important;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
        margin-top: 0px !important;
        margin-bottom: 20px !important;
        display: block;
        width: 100%;
    }

    h4 {
        color: #00FFCC !important;
        font-size: 2rem !important;
        font-weight: 900 !important;
        border-bottom: 4px solid #00FFCC;
        display: table;
        margin-bottom: 15px !important;
    }

    /* תיקון סופי לצ'קבוקסים - הזזת הריבוע לימין */
    [data-testid="stCheckbox"] > label {
        flex-direction: row-reverse !important;
        width: 100% !important;
        justify-content: flex-start !important;
        gap: 15px !important;
    }
    
    [data-testid="stCheckbox"] {
        border: none !important;
    }

    /* טקסטים לבנים בוהקים */
    p, span, label, .stMarkdown {
        color: #FFFFFF !important;
        font-weight: 800 !important;
        font-size: 1.3rem !important;
    }

    /* עיצוב תיבות קלט (לינק ומספרים) */
    input {
        background-color: #111 !important;
        color: #00FFCC !important;
        font-size: 1.3rem !important;
        border: 2px solid #333 !important;
        text-align: right !important;
    }

    /* כפתור הרצה */
    .stButton button {
        width: 100%;
        background-color: #00FFCC !important;
        color: #000 !important;
        font-size: 2.5rem !important;
        font-weight: 900 !important;
        height: 80px !important;
        border-radius: 0px !important;
        border: none !important;
        margin-top: 20px;
    }

    /* התאמה לנייד */
    @media (max-width: 640px) {
        .main-title { font-size: 4rem !important; }
        .sub-title { font-size: 1.5rem !important; }
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title">AUDITOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">מערכת אימות אמינות משתמשים</div>', unsafe_allow_html=True)

    # --- שדה לינק חדש ---
    st.markdown("#### 🔗 לינק לסרטון הנבדק")
    video_url = st.text_input("הדבק כאן את הלינק (TikTok / Instagram)", placeholder="https://www.tiktok.com/@user/video/...")

    # --- חלק א' ---
    st.write("")
    st.markdown("#### 📊 מדד אמינות קהילה")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים בחשבון", min_value=0, value=1000)
    with col2:
        likes = st.number_input("לייקים ממוצעים", min_value=0, value=10)
    
    er = (likes / followers) * 100 if followers > 0 else 0
    
    if er < 1:
        st.markdown(f"🔴 **רמת סנכרון קהל נמוכה מאוד: {er:.2f}%**")
    else:
        st.markdown(f"🟢 **רמת סנכרון קהל: {er:.2f}%**")

    # --- חלק ב' ---
    st.write("")
    st.markdown("#### 🚩 דגלי אמינות")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'ללא מאמץ'")
    q2 = st.checkbox("מפגן עושר מוגזם (מזויף/שכור)")
    q3 = st.checkbox("יצירת בהלה ולחץ זמן")
    q4 = st.checkbox("זהות מטושטשת / אין פנים לעסק")
    q5 = st.checkbox("הפניה לערוצים לא רשמיים (טלגרם)")
    q6 = st.checkbox("חסימת ביקורת ותגובות")

    # חישוב
    score = 0
    if er < 1 and followers > 2000: score += 35
    if q1: score += 25
    if q2: score += 15
    if q3: score += 15
    if q4: score += 20
    if q5: score += 15
    if q6: score += 10
    final_score = min(score, 100)

    st.write("")
    if st.button("בצע אימות"):
        if not video_url:
            st.warning("שים לב: לא הוזן לינק לסרטון, אך נבצע ניתוח לפי הנתונים שהזנת.")
            
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            number = {'font': {'color': "#FFFFFF", 'size': 60}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF", 'tickwidth': 3},
                'bar': {'color': "#FF0000" if final_score > 50 else "#00FFCC"},
                'bgcolor': "#111111",
                'steps': [
                    {'range': [0, 50], 'color': "#003322"},
                    {'range': [50, 100], 'color': "#330000"}
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=350)
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("❌ אזהרה: נמצאה התאמה גבוהה לדפוס הונאה!")
        elif final_score > 25:
            st.warning("⚠️ חשד: קיימים ליקויים באמינות המפרסם.")
        else:
            st.success("💎 אימות עבר בהצלחה: לא נמצאו דגלים אדומים.")

if __name__ == "__main__":
    main()
