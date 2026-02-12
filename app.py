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
    
    /* תיבת טיפ חכם */
    .insight-box {
        border: 2px solid #00FFCC;
        background-color: rgba(0, 255, 204, 0.05);
        padding: 15px;
        margin-top: 15px;
        border-radius: 8px;
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

    video_url = st.text_input("🔗 לינק לסרטון", placeholder="הדבק כאן לינק לבדיקה")

    st.write("")
    st.markdown("#### 📊 מדדי מעורבות")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים בחשבון", min_value=1, value=1000)
        comments = st.number_input("תגובות לסרטון", min_value=0, value=10)
    with col2:
        likes = st.number_input("לייקים לסרטון", min_value=0, value=100)

    # לוגיקה
    er = (likes / followers) * 100
    talkability = (comments / likes) * 100 if likes > 0 else 0
    
    st.write("")
    st.markdown("#### 🚩 דגלי אמינות")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'ללא מאמץ'")
    q2 = st.checkbox("מפגן עושר מוגזם (מכוניות/מזומן)")
    q3 = st.checkbox("לחץ זמן מניפולטיבי ('נותרו מקומות')")
    q4 = st.checkbox("חוסר שקיפות / אין פנים לעסק")
    q5 = st.checkbox("הפניה לערוץ טלגרם/וואטסאפ")
    q6 = st.checkbox("תגובות גנריות (רק אימוג'ים)")

    # חישוב הציון
    score = 0
    insight_text = "נראה שהיוצר שומר על פרופיל אמין. תמיד כדאי להצליב נתונים עם גוגל."

    if er < 1 and followers > 5000: 
        score += 25
        insight_text = "💡 שים לב: כמות הלייקים נמוכה מאוד ביחס לכמות העוקבים. ייתכן שמדובר בחשבון עם עוקבים קנויים או 'קהל רפאים'."
    
    if likes > 500 and talkability < 0.5: 
        score += 25
        insight_text = "💡 דגל אדום: יש המון לייקים אבל כמעט אין תגובות. זהו סימן קלאסי לרכישת לייקים מזויפים מחוות בוטים."

    if q1 or q3:
        score += 25
        insight_text = "💡 זהירות: הבטחות לרווח מהיר ולחץ זמן הם הכלים המרכזיים של הונאות פיננסיות. אל תתפתה להחליט מהר."

    if q5:
        score += 15
        insight_text = "💡 שים לב: מעבר לטלגרם או וואטסאפ נועד לרוב כדי למנוע פיקוח של הרשתות החברתיות על התוכן המועבר."

    final_score = min(score, 100)

    if st.button("בצע אימות"):
        st.session_state.analyzed = True
        st.session_state.final_score = final_score
        st.session_state.insight = insight_text

    if st.session_state.analyzed:
        s = st.session_state.final_score
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = s,
            number = {'font': {'color': "#FFFFFF", 'size': 50}, 'suffix': "%"},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': "#FFFFFF"},
                'bar': {'color': "#FF0000" if s > 50 else "#00FFCC"},
                'bgcolor': "#111111",
                'steps': [{'range': [0, 50], 'color': "#003322"}, {'range': [50, 100], 'color': "#330000"}],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(t=0, b=0))
        st.plotly_chart(fig)

        # תיבת הטיפ החכם
        st.markdown(f'<div class="insight-box">{st.session_state.insight}</div>', unsafe_allow_html=True)

        app_url = "https://auditor-app-7clswzggcjo9setfbyetqi.streamlit.app"
        msg = f"בדקתי סרטון ב-AUDITOR וקיבלתי מדד סיכון של {s}%! 🛡️\nתבדקו גם אתם:\n{app_url}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-button">שתף תוצאה בוואטסאפ 📱</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
