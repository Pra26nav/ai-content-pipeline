import streamlit as st
import json, os

st.set_page_config(page_title="Leaderboard", page_icon="🏆", layout="wide")

import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.json")
RATINGS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ratings.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def load_ratings():
    if os.path.exists(RATINGS_FILE):
        with open(RATINGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_ratings(ratings):
    with open(RATINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(ratings, f, indent=2)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.page-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #1a1a2e; }
.page-sub { color: #888; font-size: 0.9rem; margin-bottom: 2rem; }
.rank-card { background: white; border: 1px solid #e0dcff; border-radius: 14px; padding: 1.2rem 1.5rem; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; }
.rank-num { font-family: 'Syne', sans-serif; font-size: 1.5rem; font-weight: 800; color: #7c6af7; min-width: 2rem; }
.rank-topic { font-family: 'Syne', sans-serif; font-weight: 600; color: #1a1a2e; font-size: 0.95rem; }
.rank-meta { color: #888; font-size: 0.8rem; }
.stars { color: #f4b942; font-size: 1.1rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🏆 Content Leaderboard</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Rate your content pieces. Top-rated rise to the top.</div>', unsafe_allow_html=True)

history = load_history()
ratings = load_ratings()

if not history:
    st.info("No content yet. Generate some content first in the App!")
else:
    # Rating section
    st.markdown("### ⭐ Rate Your Content")
    for entry in history:
        eid = entry["id"]
        current = ratings.get(eid, {}).get("stars", 0)
        with st.expander(f"{'⭐'*current if current else '☆'} {entry['topic'][:50]} — {entry['format']} · {entry['timestamp']}"):
            st.markdown(f"**Tone:** {entry['tone']}")
            st.markdown(entry['output'][:250] + "...")
            stars = st.slider("Rate this piece", 1, 5, max(current, 1), key=f"star_{eid}")
            if st.button("Save Rating", key=f"save_{eid}"):
                ratings[eid] = {
                    "stars": stars,
                    "topic": entry["topic"],
                    "format": entry["format"],
                    "timestamp": entry["timestamp"]
                }
                save_ratings(ratings)
                st.success("Rating saved!")
                st.rerun()

    # Leaderboard
    st.markdown("---")
    st.markdown("### 🏆 Top Rated Content")

    rated = [(eid, data) for eid, data in ratings.items() if data.get("stars", 0) > 0]
    rated.sort(key=lambda x: x[1]["stars"], reverse=True)

    if not rated:
        st.info("Rate some content above to see the leaderboard!")
    else:
        medals = ["🥇", "🥈", "🥉"]
        for i, (eid, data) in enumerate(rated[:10]):
            medal = medals[i] if i < 3 else f"#{i+1}"
            stars_display = "⭐" * data["stars"]
            st.markdown(f"""
            <div class="rank-card">
                <div class="rank-num">{medal}</div>
                <div style="flex:1">
                    <div class="rank-topic">{data['topic'][:60]}</div>
                    <div class="rank-meta">{data['format']} · {data['timestamp']}</div>
                </div>
                <div class="stars">{stars_display}</div>
            </div>
            """, unsafe_allow_html=True)