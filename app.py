import streamlit as st
import plotly.graph_objects as go

# ---------- הגדרות דף ----------
st.set_page_config(
    page_title="The Authenticity Auditor | בדיקת אמינות",
    page_icon="🛡️",
    layout="centered",
)

# ---------- עיצוב RTL ועברית ----------
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    html, body, [class*="st-"] {
        direction: RTL;
        text-align: right;
        font-family: 'Assistant', sans-serif;
    }
    .stApp {
        background: radial-gradient(circle at top, #0f172a 0, #020617 100%);
        color: #e5e7eb;
    }
    .main-card {
        background: rgba(30, 41, 59, 0.7);
        padding: 2rem;
        border-radius: 15px;
        border: 1px solid rgba(255,255,255,0.1);
        margin-bottom: 2rem;
    }
    .stNumberInput label, .stRadio label {
        color: #9ca3af !important;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

def calculate_risk(followers, likes, comments, questions_score):
    risk_score = questions_score
    
    # חישוב Engagement Rate
    if followers > 0:
        er = (likes + comments) / followers
        # אם ה-ER נמוך מ-1% בחשבון גדול, זה חשוד
        if followers > 5000 and er < 0.01:
            risk_score += 20
    
    return min(risk_score, 100)

def main():
    st.title("🛡️ The Authenticity Auditor")
    st.subheader("כלי לבדיקת אמינות סרטוני השקעות והזדמנויות עסקיות")
    
    st.markdown('<div class="main-card">', unsafe_allow_html=True)
    
    # --- שלב 1: נתונים יבשים ---
    st.write("### 1. נתונים יבשים מהפרופיל")
    col1, col2, col3 = st.columns(3)
    with col1:
        followers = st.number_input("מספר עוקבים", min_value=0, value=0)
    with col2:
        likes = st.number_input("לייקים ממוצע לסרטון", min_value=0, value=0)
    with col3:
        comments = st.number_input("כמות תגובות", min_value=0, value=0)

    st.write("---")

    # --- שלב 2: שאלון אדום ---
    st.write("### 2. סימנים אדומים (Red Flags)")
    
    q1 = st.radio("האם ההבטחה נשמעת 'טובה מכדי להיות אמיתית'? (כסף קל, תשואה מובטחת)", ["לא", "אולי", "כן"])
    q2 = st.radio("האם התגובות סגורות או נראות מוגבלות מאוד?", ["לא", "אולי", "כן"])
    q3 = st.radio("האם יש לחץ זמן קיצוני? ('נשארו מקומות אחרונים', 'עוד 5 דקות הלינק נסגר')", ["לא", "אולי", "כן"])
    q4 = st.radio("האם היוצר מפנה אתכם לשיחה פרטית בטלגרם או בוואטסאפ במקום אתר רשמי?", ["לא", "אולי", "כן"])

    # חישוב ציון שאלון
    mapping = {"לא": 0, "אולי": 10, "כן": 20}
    questions_score = mapping[q1] + mapping[q2] + mapping[q3] + mapping[q4]
    
    st.markdown('</div>', unsafe_allow_html=True)

    # --- שלב 3: תוצאות ---
    if st.button("נתח רמת סיכון"):
        final_score = calculate_risk(followers, likes, comments, questions_score)
        
        # בניית מד ה-Gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = final_score,
            title = {'text': "מדד סיכון (Risk Score)"},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "#ef4444" if final_score > 60 else "#f59e0b" if final_score > 30 else "#10b981"},
                'steps': [
                    {'range': [0, 30], 'color': "rgba(16, 185, 129, 0.2)"},
                    {'range': [30, 60], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [60, 100], 'color': "rgba(239, 68, 68, 0.2)"}
                ],
            }
        ))
        
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font={'color': "white", 'family': "Assistant"})
        st.plotly_chart(fig)

        if final_score > 60:
            st.error("⚠️ רמת סיכון גבוהה! מומלץ להתרחק ולבדוק היטב מי עומד מאחורי ההצעה.")
        elif final_score > 30:
            st.warning("🧐 ישנם סימנים חשודים. כדאי להצליב נתונים ולא לקבל החלטה פזיזה.")
        else:
            st.success("✅ נראה תקין יחסית, אך תמיד יש להפעיל שיקול דעת עצמאי.")

if __name__ == "__main__":
    main()
