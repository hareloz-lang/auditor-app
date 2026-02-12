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
    st.markdown('<div class="sub-title">מערכת אימות אמינות (Dynamic Benchmark)</div>', unsafe_allow_html=True)

    st.text_input("🔗 לינק לסרטון", placeholder="הדבק כאן לינק לבדיקה")

    st.write("")
    st.markdown("#### 📊 מדדי מעורבות")
    col1, col2 = st.columns(2)
    with col1:
        followers = st.number_input("עוקבים בחשבון", min_value=1, value=1000)
        comments = st.number_input("תגובות לסרטון", min_value=0, value=10)
    with col2:
        likes = st.number_input("לייקים לסרטון", min_value=0, value=100)

    # --- חישובי אלגוריתם ---
    er = (likes / followers) * 100
    talkability = (comments / likes) * 100 if likes > 0 else 0
    
    # הגדרת בנצ'מרק דינמי לפי גודל חשבון
    if followers < 10000:
        er_threshold = 4.0  # חשבון קטן חייב מעורבות גבוהה
        category = "Micro"
    elif followers < 100000:
        er_threshold = 2.0
        category = "Mid-Size"
    else:
        er_threshold = 0.8  # חשבון גדול מקבל "הנחה"
        category = "Macro"

    st.write("")
    st.markdown("#### 🚩 דגלי אמינות")
    q1 = st.checkbox("הבטחה לכסף מהיר / 'ללא מאמץ'")
    q2 = st.checkbox("מפגן עושר מוגזם (מכוניות/מזומן)")
    q3 = st.checkbox("לחץ זמן מניפולטיבי ('נותרו מקומות')")
    q4 = st.checkbox("חוסר שקיפות / אין פנים לעסק")
    q5 = st.checkbox("הפניה לערוץ טלגרם/וואטסאפ")
    q6 = st.checkbox("תגובות גנריות (רק אימוג'ים)")

    # חישוב ציון משוקלל
    score = 0
    insight_note = "(הנתונים נראים בטווח הנורמה לקטגוריה זו)"

    # קנס ER דינמי
    if er < er_threshold:
        score += 30
        insight_note = f"(התראה: יחס המעורבות נמוך מהבנצ'מרק של {er_threshold}% לחשבונות {category})"
    
    # קנס Talkability (לייקים ללא תגובות)
    if likes > 500 and talkability < 0.6: 
        score += 25
        insight_note = "(דגל אדום: חוסר תואם קיצוני בין לייקים לתגובות - חשד לזיוף מעורבות)"

    if q1 or q3:
        score += 20
        insight_note = "(קריטריון פסיכולוגי: המפרסם משתמש במניפולציות של דחיפות ורווח מהיר)"

    if q5:
        score += 15
        insight_note = "(הערה טכנית: מעבר לפלטפורמות חיצוניות ללא פיקוח מגדיל את הסיכון למשתמש)"

    final_score = min(score, 100)

    if st.button("בצע אימות"):
        st.session_state.analyzed = True
        st.session_state.final_score = final_score
        st.session_state.insight = insight_note

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

        if s > 65:
            st.error(f"❌ אזהרה: מדד סיכון חריג של {s}%")
        elif s > 30:
            st.warning("⚠️ חשד: המערכת זיהתה ליקויים באמינות המפרסם.")
        else:
            st.success("💎 אימות עבר בהצלחה. המדדים אורגניים.")

        st.markdown(f'<div class="insight-box">תובנת AUDITOR: {st.session_state.insight}</div>', unsafe_allow_html=True)

        app_url = "https://auditor-app-7clswzggcjo9setfbyetqi.streamlit.app"
        msg = f"בדקתי סרטון ב-AUDITOR וקיבלתי מדד סיכון של {s}%! 🛡️\n{app_url}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(msg)}"
        st.markdown(f'<a href="{whatsapp_url}" target="_blank" class="whatsapp-button">שתף תוצאה בוואטסאפ 📱</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
