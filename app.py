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
    .sub-title { color: #FFFFFF !important; font-size: 1.8rem !important; font-weight: 800 !important; margin-bottom: 20px !important; }
    h4 { color: #00FFCC !important; font-size: 2rem !important; font-weight: 900 !important; border-bottom: 4px solid #00FFCC; display: inline-block; margin-bottom: 15px !important; }
    [data-testid="stCheckbox"] label { display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 10px !important; background: #111; margin-bottom: 5px; border-radius: 4px; }
    p, span, label, .stMarkdown { color: #FFFFFF !important; font-weight: 800 !important; font-size: 1.2rem !important; }
    input { background-color: #111 !important; color: #00FFCC !important; font-size: 1.3rem !important; border: 2px solid #333 !important; }
    .stButton button { width: 100%; background-color: #00FFCC !important; color: #000 !important; font-size: 2.5rem !important; font-weight: 900 !important; height: 80px !important; border-radius: 0px !important; border: none !important; margin-top: 20px; }
    
    /* עיצוב כפתור וואטסאפ */
    .whatsapp-button {
        display: inline-block;
        background-color: #25D366;
        color: white !important;
        padding: 15px 30px;
        text-decoration: none;
        font-size: 1.5rem;
        font-weight: bold;
        border-radius: 50px;
        text-align: center;
        width: 100%;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.markdown('<div class="main-title">AUDITOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">מערכת אימות אמינות משתמשים</div>', unsafe_allow_html=True)

    st.markdown("#### 🔗 לינק לסרטון")
    video_url = st.text_input("", placeholder="הדבק לינק מ-TikTok / Instagram כאן")

    st.write("")
    st.markdown("#### 📊 מדד אמינות קהילה")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים", min_value=0, value=1000)
    with col2:
        likes = st.number_input("לייקים", min_value=0, value=10)
    
    er = (likes / followers) * 100 if followers > 0 else 0
    if er < 1:
        st.markdown(f"🔴 **סנכרון קהל נמוך: {er:.2f}%**")
    else:
        st.markdown(f"🟢 **סנכרון קהל: {er:.2f}%**")

    st.write("")
    st.markdown("#### 🚩 דגלי אמינות")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'ללא מאמץ'")
    q2 = st.checkbox("מפגן עושר מוגזם (מזויף/שכור)")
    q3 = st.checkbox("יצירת בהלה ולחץ זמן")
    q4 = st.checkbox("זהות מטושטשת / אין פנים")
    q5 = st.checkbox("הפניה לערוצים לא רשמיים")
    q6 = st.checkbox("חסימת ביקורת ותגובות")

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
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            number = {'font': {'color': "#FFFFFF", 'size': 60}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF", 'tickwidth': 3},
                'bar': {'color': "#FF0000" if final_score > 50 else "#00FFCC"},
                'bgcolor': "#111111",
                'steps': [{'range': [0, 50], 'color': "#003322"}, {'range': [50, 100], 'color': "#330000"}],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(t=0, b=0))
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("❌ אזהרה: נמצאה התאמה גבוהה לדפוס הונאה!")
        elif final_score > 25:
            st.warning("⚠️ חשד: קיימים ליקויים באמינות.")
        else:
            st.success("💎 אימות עבר בהצלחה.")

        # --- יצירת לינק שיתוף לוואטסאפ ---
       app_url = https://auditor-app-7clswzggcjo9setfbyetqi.streamlit.app = "https://auditor-app.streamlit.app" # שנה ללינק האמיתי שלך
        msg = f"בדקתי סרטון ב-AUDITOR וקיבלתי מדד סיכון של {final_score}%! 🛡️\nמומלץ לבדוק לפני שמאמינים למפרסמים ברשת:\n{app_url}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-button">שתף תוצאה בוואטסאפ 📱</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
