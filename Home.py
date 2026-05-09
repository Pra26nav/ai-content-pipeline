import streamlit as st

st.set_page_config(page_title="AI Content Pipeline", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.stApp { background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

.nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; border-bottom: 1px solid #e0dcff; background: white; position: sticky; top: 0; z-index: 100; }
.nav-logo { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800; color: #7c6af7; }
.nav-links a { margin-left: 2rem; color: #555; text-decoration: none; font-size: 0.9rem; font-weight: 500; }
.nav-links a:hover { color: #7c6af7; }

.hero-section { text-align: center; padding: 6rem 2rem 4rem 2rem; }
.hero-section h1 { font-family: 'Syne', sans-serif; font-size: 3.5rem; font-weight: 800; background: linear-gradient(90deg, #5b4fd4, #7c6af7, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 1rem; }
.hero-section p { font-size: 1.15rem; color: #666; max-width: 600px; margin: 0 auto 2rem auto; line-height: 1.7; }

.cta-btn { display: inline-block; background: linear-gradient(135deg, #7c6af7, #5b4fd4); color: white !important; padding: 0.85rem 2.5rem; border-radius: 12px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; text-decoration: none; margin-right: 1rem; }
.cta-btn-outline { display: inline-block; border: 2px solid #7c6af7; color: #7c6af7 !important; padding: 0.85rem 2.5rem; border-radius: 12px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 1rem; text-decoration: none; }

.features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; padding: 4rem 4rem; max-width: 1100px; margin: 0 auto; }
.feature-card { background: white; border: 1px solid #e0dcff; border-radius: 16px; padding: 2rem; text-align: center; }
.feature-card h3 { font-family: 'Syne', sans-serif; color: #7c6af7; margin-bottom: 0.5rem; }
.feature-card p { color: #666; font-size: 0.9rem; line-height: 1.6; }
.feature-icon { font-size: 2rem; margin-bottom: 1rem; }

.badge { display: inline-block; background: #ede9ff; color: #7c6af7; padding: 0.3rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 600; margin-bottom: 1.5rem; }
</style>
""", unsafe_allow_html=True)

# NAV
st.markdown("""
<div class="nav">
    <div class="nav-logo">✦ AI Content Pipeline</div>
    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/Pricing">Pricing</a>
        <a href="/Signup">Sign Up</a>
        <a href="/App" style="color:#7c6af7; font-weight:700;">Launch App →</a>
    </div>
</div>
""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero-section">
    <div class="badge">✦ Powered by CrewAI + Groq</div>
    <h1>Content that writes<br>itself. Almost.</h1>
    <p>Three autonomous AI agents research, write, and edit publication-ready content in minutes. Blog posts, LinkedIn, Twitter threads, newsletters — all from a single topic.</p>
    <a class="cta-btn" href="/App">Start Creating Free →</a>
    <a class="cta-btn-outline" href="/Pricing">View Pricing</a>
</div>
""", unsafe_allow_html=True)

# FEATURES
st.markdown("""
<div class="features">
    <div class="feature-card">
        <div class="feature-icon">🔍</div>
        <h3>Real-Time Research</h3>
        <p>Researcher agent searches the live web for current facts, trends and examples — not just LLM knowledge.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">✍️</div>
        <h3>Multi-Format Output</h3>
        <p>Blog posts, LinkedIn posts, Twitter threads, email newsletters — same topic, different formats instantly.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">✨</div>
        <h3>AI Editor Included</h3>
        <p>Every piece goes through an AI editor that fixes flow, phrasing, and tone before you see it.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <h3>Groq-Powered Speed</h3>
        <p>Llama 3.3 70B via Groq delivers results in seconds — no waiting, no throttling.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🕘</div>
        <h3>History Log</h3>
        <p>Every run is saved. Reload, download, or compare past outputs from the sidebar anytime.</p>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <h3>Keyword & Tone Control</h3>
        <p>Add focus keywords, references, tone, and word count. Full control over what agents produce.</p>
    </div>
</div>
""", unsafe_allow_html=True)