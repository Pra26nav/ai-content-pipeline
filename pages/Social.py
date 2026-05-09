import streamlit as st

st.set_page_config(page_title="Social Connect", page_icon="🔗", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.page-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #1a1a2e; }
.page-sub { color: #888; font-size: 0.9rem; margin-bottom: 2rem; }
.social-card { background: white; border: 1px solid #e0dcff; border-radius: 16px; padding: 2rem; text-align: center; position: relative; }
.social-card h3 { font-family: 'Syne', sans-serif; font-size: 1.1rem; font-weight: 700; margin: 1rem 0 0.3rem 0; }
.social-card p { color: #888; font-size: 0.85rem; margin-bottom: 1.5rem; }
.social-icon { font-size: 2.5rem; }
.connect-btn { display: inline-block; background: linear-gradient(135deg, #7c6af7, #5b4fd4); color: white; padding: 0.6rem 1.5rem; border-radius: 10px; font-family: 'Syne', sans-serif; font-weight: 700; font-size: 0.85rem; text-decoration: none; }
.coming-soon { position: absolute; top: 12px; right: 12px; background: #ede9ff; color: #7c6af7; font-size: 0.65rem; font-weight: 700; font-family: 'Syne', sans-serif; padding: 0.2rem 0.6rem; border-radius: 20px; letter-spacing: 1px; text-transform: uppercase; }
.benefit-row { display: flex; align-items: flex-start; gap: 0.8rem; margin-bottom: 1rem; }
.benefit-icon { font-size: 1.2rem; min-width: 1.5rem; }
.benefit-text { font-size: 0.88rem; color: #444; line-height: 1.5; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🔗 Social Connect</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Connect your social accounts to publish content directly — coming soon.</div>', unsafe_allow_html=True)

# Platform cards
col1, col2, col3, col4 = st.columns(4)

platforms = [
    (col1, "𝕏", "Twitter / X", "Schedule threads, track impressions and engagement directly."),
    (col2, "in", "LinkedIn", "Publish posts and monitor reach, likes, and comments."),
    (col3, "📸", "Instagram", "Caption generation and story scheduling."),
    (col4, "📘", "Facebook", "Page post scheduling and audience analytics."),
]

for col, icon, name, desc in platforms:
    with col:
        st.markdown(f"""
        <div class="social-card">
            <div class="coming-soon">Coming Soon</div>
            <div class="social-icon">{icon}</div>
            <h3>{name}</h3>
            <p>{desc}</p>
            <span class="connect-btn" style="opacity:0.5; cursor:not-allowed;">Connect →</span>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)

# What you'll get section
st.markdown("### 🚀 What Social Connect Will Enable")
col_a, col_b = st.columns(2)

benefits_left = [
    ("📤", "One-click publish — generate content and post directly to your connected platforms"),
    ("📊", "Real engagement data — see likes, views, shares pulled live from each platform"),
    ("🗓️", "Auto-schedule — queue posts to your content calendar without leaving the app"),
]
benefits_right = [
    ("🏆", "Leaderboard powered by real data — ranked by actual engagement, not just ratings"),
    ("🔔", "Streak alerts — get notified when your posting streak is about to break"),
    ("🤖", "AI suggestions — agent recommends best time to post based on your audience data"),
]

with col_a:
    for icon, text in benefits_left:
        st.markdown(f'<div class="benefit-row"><div class="benefit-icon">{icon}</div><div class="benefit-text">{text}</div></div>', unsafe_allow_html=True)
with col_b:
    for icon, text in benefits_right:
        st.markdown(f'<div class="benefit-row"><div class="benefit-icon">{icon}</div><div class="benefit-text">{text}</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# Waitlist
st.markdown("### 📬 Join the Waitlist")
col_x, col_y, col_z = st.columns([2, 1, 3])
with col_x:
    email = st.text_input("Your email", placeholder="you@example.com")
with col_y:
    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
    if st.button("Join Waitlist"):
        if email:
            st.success(f"✦ {email} added to waitlist!")
        else:
            st.error("Enter your email first.")