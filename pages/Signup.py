import streamlit as st

st.set_page_config(page_title="Sign Up — AI Content Pipeline", page_icon="✦", layout="centered")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

.nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; border-bottom: 1px solid #e0dcff; background: white; margin-bottom: 3rem; }
.nav-logo { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800; color: #7c6af7; }
.nav-links a { margin-left: 2rem; color: #555; text-decoration: none; font-size: 0.9rem; }

.signup-box { max-width: 480px; margin: 0 auto; background: white; border: 1px solid #e0dcff; border-radius: 20px; padding: 3rem 2.5rem; }
.signup-box h1 { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #1a1a2e; margin-bottom: 0.3rem; }
.signup-box p { color: #888; font-size: 0.9rem; margin-bottom: 2rem; }

.stTextInput label { color: #7c6af7 !important; font-weight: 500 !important; }
.stTextInput > div > div > input { border: 1.5px solid #7c6af7 !important; border-radius: 10px !important; padding: 0.75rem 1rem !important; }
.stButton > button { background: linear-gradient(135deg, #7c6af7, #5b4fd4) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 700 !important; width: 100% !important; padding: 0.75rem !important; margin-top: 0.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav">
    <div class="nav-logo">✦ AI Content Pipeline</div>
    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/Pricing">Pricing</a>
        <a href="/Signup" style="color:#7c6af7;">Sign Up</a>
        <a href="/App">Launch App →</a>
    </div>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align:center; margin-bottom:2rem;">
        <div style="font-family:Syne,sans-serif; font-size:2rem; font-weight:800; color:#1a1a2e;">Create your account</div>
        <p style="color:#888; font-size:0.9rem; margin-top:0.3rem;">Start generating content in 60 seconds</p>
    </div>
    """, unsafe_allow_html=True)

    name = st.text_input("Full Name", placeholder="Pranav Sharma")
    email = st.text_input("Email", placeholder="you@example.com")
    password = st.text_input("Password", placeholder="Min 8 characters", type="password")

    plan = st.selectbox("Select Plan", ["Free", "Pro — ₹499/mo", "Team — ₹1999/mo"])

    if st.button("✦ Create Account"):
        if name and email and password:
            st.success(f"Welcome, {name}! Account created. Head to the App to start generating.")
            st.balloons()
        else:
            st.error("Please fill all fields.")

    st.markdown("""
    <p style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:1.5rem;">
        Already have an account? <a href="/App" style="color:#7c6af7;">Sign in →</a>
    </p>
    """, unsafe_allow_html=True)