import streamlit as st

st.set_page_config(page_title="Pricing — AI Content Pipeline", page_icon="✦", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}

.nav { display: flex; justify-content: space-between; align-items: center; padding: 1rem 2rem; border-bottom: 1px solid #e0dcff; background: white; }
.nav-logo { font-family: 'Syne', sans-serif; font-size: 1.2rem; font-weight: 800; color: #7c6af7; }
.nav-links a { margin-left: 2rem; color: #555; text-decoration: none; font-size: 0.9rem; font-weight: 500; }

.pricing-hero { text-align: center; padding: 4rem 2rem 3rem 2rem; }
.pricing-hero h1 { font-family: 'Syne', sans-serif; font-size: 2.8rem; font-weight: 800; color: #1a1a2e; }
.pricing-hero p { color: #666; font-size: 1rem; margin-top: 0.5rem; }

.plans { display: grid; grid-template-columns: repeat(3, 1fr); gap: 2rem; max-width: 1000px; margin: 0 auto; padding: 2rem 4rem 4rem 4rem; }
.plan { background: white; border: 1px solid #e0dcff; border-radius: 20px; padding: 2.5rem 2rem; text-align: center; }
.plan.popular { border: 2px solid #7c6af7; position: relative; }
.popular-badge { position: absolute; top: -14px; left: 50%; transform: translateX(-50%); background: #7c6af7; color: white; padding: 0.2rem 1rem; border-radius: 20px; font-size: 0.75rem; font-weight: 700; font-family: 'Syne', sans-serif; }
.plan h2 { font-family: 'Syne', sans-serif; color: #1a1a2e; margin-bottom: 0.5rem; }
.plan .price { font-family: 'Syne', sans-serif; font-size: 2.5rem; font-weight: 800; color: #7c6af7; }
.plan .price span { font-size: 1rem; font-weight: 400; color: #999; }
.plan ul { list-style: none; padding: 0; margin: 1.5rem 0; text-align: left; }
.plan ul li { padding: 0.4rem 0; color: #555; font-size: 0.9rem; }
.plan ul li::before { content: "✓ "; color: #7c6af7; font-weight: 700; }
.plan-btn { display: block; background: linear-gradient(135deg, #7c6af7, #5b4fd4); color: white; padding: 0.75rem; border-radius: 10px; font-family: 'Syne', sans-serif; font-weight: 700; text-decoration: none; margin-top: 1rem; }
.plan-btn.outline { background: transparent; border: 2px solid #7c6af7; color: #7c6af7; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="nav">
    <div class="nav-logo">✦ AI Content Pipeline</div>
    <div class="nav-links">
        <a href="/">Home</a>
        <a href="/Pricing" style="color:#7c6af7;">Pricing</a>
        <a href="/Signup">Sign Up</a>
        <a href="/App">Launch App →</a>
    </div>
</div>

<div class="pricing-hero">
    <h1>Simple, honest pricing</h1>
    <p>Start free. Scale when you're ready.</p>
</div>

<div class="plans">
    <div class="plan">
        <h2>Free</h2>
        <div class="price">₹0 <span>/mo</span></div>
        <ul>
            <li>10 generations/month</li>
            <li>Blog & LinkedIn formats</li>
            <li>Basic keyword control</li>
            <li>History log (last 5)</li>
            <li>Download as .md</li>
        </ul>
        <a class="plan-btn outline" href="/Signup">Get Started</a>
    </div>
    <div class="plan popular">
        <div class="popular-badge">Most Popular</div>
        <h2>Pro</h2>
        <div class="price">₹499 <span>/mo</span></div>
        <ul>
            <li>Unlimited generations</li>
            <li>All 4 output formats</li>
            <li>Real-time web research</li>
            <li>Full history log</li>
            <li>Priority Groq speed</li>
            <li>Download .md + .docx</li>
        </ul>
        <a class="plan-btn" href="/Signup">Start Pro</a>
    </div>
    <div class="plan">
        <h2>Team</h2>
        <div class="price">₹1999 <span>/mo</span></div>
        <ul>
            <li>Everything in Pro</li>
            <li>5 team seats</li>
            <li>Shared history log</li>
            <li>Custom tone profiles</li>
            <li>API access</li>
            <li>Priority support</li>
        </ul>
        <a class="plan-btn outline" href="/Signup">Contact Us</a>
    </div>
</div>
""", unsafe_allow_html=True)