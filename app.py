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
    .main-title { color: #00FFCC !important; font-size: clamp(3rem, 10vw, 6rem) !important; font-weight: 900 !important; line-height: 0.8 !important; margin-bottom: 5px !important; letter-spacing: -2px; text-align: right; }
    .sub-title { color: #FFFFFF !important; font-size: 1.8rem !important; font-weight: 800 !important; margin-bottom: 20px !important; text-align: right; }
    h4 { color: #00FFCC !important; font-size: 1.8rem !important; font-weight: 900 !important; border-bottom: 4px solid #00FFCC; display: inline-block; margin-bottom: 15px !important; }
    [data-testid="stCheckbox"] label { display: flex !important; flex-direction: row !important; justify-content: space-between !important; align-items: center !important; padding: 10px !important; background: #111; margin-bottom: 5px; border-radius: 4px; }
    p, span, label, .stMarkdown { color: #FFFFFF !important; font-weight: 800 !important; font-size: 1.1rem !important; }
    input { background-color: #111 !important; color: #00FFCC !important; font-size: 1.2rem !important; border: 2px solid #333 !important; text-align: right !important; }
    .stButton button { width: 100%; background-color: #00FFCC !important; color: #000 !important; font-size: 2.2rem !important; font-weight: 900 !important; height: 70px !important; border-radius: 0px !important; border: none !important; margin-top: 20px; }
    .whatsapp-button { display: block; background-color: #25D366; color: white !important; padding: 15px 20px; text-decoration: none; font-size: 1.4rem; font-weight: 900; border-radius: 5px; text-align: center; width: 100%; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

def main():
    if 'analyzed' not in st.session_state:
        st.session_state.analyzed = False
        st.session_state.final_score = 0

    st.markdown('<div class="main-title">AUDITOR</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-title">מערכת אימות אמינות משתמשים</div>', unsafe_allow_html=True)

    st.markdown("#### 🔗 לינק לסרטון")
    st.text_input("", placeholder="הדבק כאן את הלינק לבדיקה")

    st.write("")
    st.markdown("#### 📊 מדדי מעורבות (Engagement)")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים בחשבון", min_value=1, value=1000)
        comments = st.number_input("תגובות לסרטון", min_value=0, value=10)
    with col2:
        likes = st.number_input("לייקים לסרטון", min_value=0, value=100)
        st.write("") # מרווח קטן

    # לוגיקה מתמטית לשקלול
    er = (likes / followers) * 100
    talkability = (comments / likes) * 100 if likes > 0 else 0
    
    # תצוגת נתונים יבשים
    st.write(f"סנכרון קהל (ER): {er:.2f}%")
    st.write(f"מדד דיבור (תגובות/לייקים): {talkability:.2f}%")

    st.write("")
    st.markdown("#### 🚩 דגלי אמינות (סימון ידני)")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'ללא מאמץ'")
    q2 = st.checkbox("מפגן עושר מוגזם (מכוניות יוקרה/מזומן)")
    q3 = st.checkbox("לחץ זמן מניפולטיבי ('נותרו 2 מקומות')")
    q4 = st.checkbox("חוסר שקיפות / אין פנים מאחורי העסק")
    q5 = st.checkbox("הפניה לערוץ טלגרם או וואטסאפ אישי")
    q6 = st.checkbox("התגובות נראות גנריות (רק אימוג'ים)")

    # חישוב הציון המשוקלל
    score = 0
    # קנס על ER נמוך (עוקבים שלא עושים לייקים)
    if er < 1 and followers > 5000: score += 25
    # קנס על חוסר בתגובות (לייקים קנויים)
    if likes > 500 and talkability < 0.5: score += 25
    
    if q1: score += 20
    if q2: score += 15
    if q3: score += 10
    if q4: score += 15
    if q5: score += 10
    if q6: score += 15
    
    final_score = min(score, 100)

    st.write("")
    if st.button("בצע אימות"):
        st.session_state.analyzed = True
        st.session_state.final_score = final_score

    if st.session_state.analyzed:
        s = st.session_state.final_score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = s,
            number = {'font': {'color': "#FFFFFF", 'size': 55}, 'suffix': "%"},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF"},
                'bar': {'color': "#FF0000" if s > 50 else "#00FFCC"},
                'bgcolor': "#111111",
                'steps': [{'range': [0, 50], 'color': "#003322"}, {'range': [50, 100], 'color': "#330000"}],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=300, margin=dict(t=0, b=0))
        st.plotly_chart(fig)

        if s > 65:
            st.error("❌ אזהרה: רמת סיכון גבוהה מאוד. סימנים מובהקים להונאה או זיוף מעורבות.")
        elif s > 30:
            st.warning("⚠️ חשד: קיימים ליקויים באמינות. מומלץ לבדוק את התגובות לעומק.")
        else:
            st.success("💎 אימות עבר בהצלחה. המדדים נראים אורגניים ותקינים.")

        app_url = "https://auditor-app-7clswzggcjo9setfbyetqi.streamlit.app"
        msg = f"בדקתי סרטון ב-AUDITOR וקיבלתי מדד סיכון של {s}%! 🛡️\nתבדקו גם אתם לפני שמאמינים למפרסמים:\n{app_url}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-button">שתף תוצאה בוואטסאפ 📱</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
