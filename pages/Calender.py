import streamlit as st
import json, os
from datetime import datetime, timedelta
import calendar

st.set_page_config(page_title="Content Calendar", page_icon="📅", layout="wide")

# Path fix
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

HISTORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.page-title { font-family: 'DM Sans', sans-serif; font-size: 1.6rem; font-weight: 700; color: #1a1a2e; margin-bottom: 0.2rem; letter-spacing: -0.3px; border-left: 4px solid #7c6af7; padding-left: 0.8rem; }
.page-sub { color: #888; font-size: 0.9rem; margin-bottom: 2rem; }
.cal-day { background: white; border: 1px solid #e0dcff; border-radius: 10px; padding: 0.6rem; min-height: 80px; font-size: 0.75rem; }
.cal-day.has-content { border: 2px solid #7c6af7; background: #faf9ff; }
.cal-day.today { background: #7c6af7; color: white; border: 2px solid #5b4fd4; }
.cal-day .day-num { font-family: 'DM Sans', sans-serif; font-weight: 600; font-size: 0.8rem; color: #444; letter-spacing: 0.3px; }
.cal-day.today .day-num { color: white; }
.cal-day .entry-pill { background: #ede9ff; color: #7c6af7; border-radius: 6px; padding: 0.1rem 0.4rem; margin-top: 0.2rem; font-size: 0.68rem; display: block; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.streak-box { background: white; border: 2px solid #7c6af7; border-radius: 16px; padding: 1.5rem 2rem; text-align: center; }
.streak-num { font-family: 'DM Sans', sans-serif; font-size: 2.2rem; font-weight: 700; color: #7c6af7; letter-spacing: -1px; }
.streak-label { color: #6b6880; font-size: 0.78rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; }
.stat-box { background: white; border: 1px solid #e0dcff; border-radius: 12px; padding: 1.2rem; text-align: center; }
.stat-num { font-family: 'DM Sans', sans-serif; font-size: 1.6rem; font-weight: 700; color: #1a1a2e; letter-spacing: -0.5px; }
.stat-label { color: #6b6880; font-size: 0.75rem; font-weight: 500; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">📅 Content Calendar</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Track your content generation streak and posting history.</div>', unsafe_allow_html=True)

history = load_history()

# Build date → entries map
date_map = {}
for entry in history:
    try:
        dt = datetime.strptime(entry["timestamp"], "%d %b %Y, %H:%M")
        key = dt.strftime("%Y-%m-%d")
        if key not in date_map:
            date_map[key] = []
        date_map[key].append(entry)
    except:
        pass

# Streak calculation
today = datetime.now().date()
streak = 0
check = today
while True:
    if check.strftime("%Y-%m-%d") in date_map:
        streak += 1
        check -= timedelta(days=1)
    else:
        break

# Stats
total = len(history)
formats = {}
for e in history:
    formats[e.get("format", "?")] = formats.get(e.get("format", "?"), 0) + 1
top_format = max(formats, key=formats.get) if formats else "—"
active_days = len(date_map)

# Streak + stats row
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="streak-box"><div class="streak-num">🔥 {streak}</div><div class="streak-label">Day Streak</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{total}</div><div class="stat-label">Total Pieces Generated</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{active_days}</div><div class="stat-label">Active Days</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="stat-box"><div class="stat-num">{top_format[:10]}</div><div class="stat-label">Top Format</div></div>', unsafe_allow_html=True)

st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)

# Month selector
now = datetime.now()
col_a, col_b, _ = st.columns([1, 1, 4])
with col_a:
    month = st.selectbox("Month", list(range(1, 13)), index=now.month - 1, format_func=lambda x: calendar.month_name[x])
with col_b:
    year = st.selectbox("Year", [2025, 2026, 2027], index=1)

# Calendar grid
st.markdown("---")
days_header = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
cols = st.columns(7)
for i, d in enumerate(days_header):
    cols[i].markdown(f"<div style='text-align:center; font-family:Syne,sans-serif; font-size:0.75rem; font-weight:700; color:#7c6af7; padding:0.3rem;'>{d}</div>", unsafe_allow_html=True)

cal = calendar.monthcalendar(year, month)
for week in cal:
    cols = st.columns(7)
    for i, day in enumerate(week):
        if day == 0:
            cols[i].markdown("<div style='min-height:80px'></div>", unsafe_allow_html=True)
        else:
            date_str = f"{year}-{month:02d}-{day:02d}"
            entries = date_map.get(date_str, [])
            is_today = (day == today.day and month == today.month and year == today.year)

            if is_today:
                css_class = "cal-day today"
            elif entries:
                css_class = "cal-day has-content"
            else:
                css_class = "cal-day"

            pills = "".join([f'<span class="entry-pill">✦ {e["topic"][:18]}</span>' for e in entries[:2]])
            if len(entries) > 2:
                pills += f'<span class="entry-pill">+{len(entries)-2} more</span>'

            cols[i].markdown(f'<div class="{css_class}"><div class="day-num">{day}</div>{pills}</div>', unsafe_allow_html=True)

# Recent activity
st.markdown("<div style='height:2rem'></div>", unsafe_allow_html=True)
st.markdown("### 🕘 Recent Activity")
if not history:
    st.info("No content generated yet. Head to App to start!")
else:
    for entry in history[:5]:
        with st.expander(f"✦ {entry['topic']} — {entry['timestamp']}"):
            st.markdown(f"**Format:** {entry['format']} | **Tone:** {entry['tone']}")
            st.markdown(entry['output'][:300] + "...")