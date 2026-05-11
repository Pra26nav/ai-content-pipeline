import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from crewai import Crew, Process, Task
from agents import writer, editor
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "history.json")

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_to_history(topic, output_format, tone, result_text):
    history = load_history()
    entry = {
        "id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "timestamp": datetime.now().strftime("%d %b %Y, %H:%M"),
        "topic": topic + " [Remix]",
        "format": output_format,
        "tone": tone,
        "output": result_text
    }
    history.insert(0, entry)
    history = history[:20]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

st.set_page_config(page_title="Content Remix", page_icon="🔁", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; background: #f8f7ff; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
.page-title { font-family: 'Syne', sans-serif; font-size: 2rem; font-weight: 800; color: #1a1a2e; border-left: 4px solid #7c6af7; padding-left: 0.8rem; }
.page-sub { color: #888; font-size: 0.9rem; margin: 0.5rem 0 2rem 0; }
.section-label { font-family: 'Syne', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: #7c6af7; margin-bottom: 1rem; }
.content-preview { background: white; border: 1px solid #e0dcff; border-radius: 12px; padding: 1.2rem; font-size: 0.85rem; color: #444; line-height: 1.6; max-height: 200px; overflow-y: auto; }
.output-box { background: white; border: 1.5px solid #7c6af7; border-radius: 16px; padding: 2rem; margin-top: 1rem; line-height: 1.8; font-size: 0.95rem; }
.stButton > button { background: linear-gradient(135deg, #7c6af7, #5b4fd4) !important; color: white !important; border: none !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; width: 100% !important; padding: 0.75rem !important; }
.stSelectbox > div > div { border: 1.5px solid #7c6af7 !important; border-radius: 10px !important; }
.stSelectbox label { color: #7c6af7 !important; font-size: 0.82rem !important; font-weight: 500 !important; }
.stDownloadButton > button { background: transparent !important; border: 2px solid #7c6af7 !important; color: #7c6af7 !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; width: 100% !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="page-title">🔁 Content Remix</div>', unsafe_allow_html=True)
st.markdown('<div class="page-sub">Take any past content and remix it into a different format or tone — no re-research needed.</div>', unsafe_allow_html=True)

history = load_history()

if not history:
    st.info("No content yet. Generate some content in the App first!")
else:
    # Select content to remix
    st.markdown('<div class="section-label">✦ Select Content to Remix</div>', unsafe_allow_html=True)

    options = {f"{e['topic'][:50]} — {e['format']} ({e['timestamp']})": e for e in history}
    selected_label = st.selectbox("Choose a past piece:", list(options.keys()))
    selected = options[selected_label]

    st.markdown("**Preview:**")
    st.markdown(f'<div class="content-preview">{selected["output"][:500]}...</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">✦ Remix Settings</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        new_format = st.selectbox(
            "Remix into Format",
            ["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"],
            index=["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"].index(selected["format"]) if selected["format"] in ["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"] else 0
        )
    with col2:
        new_tone = st.selectbox(
            "New Tone",
            ["Informative & Conversational", "Professional & Formal", "Casual & Friendly", "Technical & In-depth"]
        )

    same_format = new_format == selected["format"]
    same_tone = new_tone == selected["tone"]

    if same_format and same_tone:
        st.warning("Select a different format or tone to remix.")

    remix = st.button("🔁 Remix Content", disabled=(same_format and same_tone))

    if remix:
        format_instructions = {
            "Blog Post": f"Rewrite as a blog post. Structure: catchy title, intro, 3-4 sections with subheadings, conclusion. Tone: {new_tone}.",
            "LinkedIn Post": f"Rewrite as a LinkedIn post. Strong hook, 3-5 short paragraphs, CTA. Max 300 words. Tone: {new_tone}. Add 5 hashtags.",
            "Twitter Thread": f"Rewrite as a Twitter/X thread. Numbered tweets (1/, 2/ etc.), 15-20 tweets, max 280 chars each. Tone: {new_tone}.",
            "Email Newsletter": f"Rewrite as an email newsletter. Subject line, greeting, intro, 3 sections, CTA, sign-off. Tone: {new_tone}.",
        }

        with st.spinner(f"Remixing into {new_format}... Writer → Editor"):
            remix_write = Task(
                description=f"""You have this existing content about '{selected['topic']}':

{selected['output']}

{format_instructions[new_format]}

Keep all the key facts and insights but completely reformat and rewrite for the new format.""",
                expected_output=f"Complete {new_format} remixed from the original content.",
                agent=writer
            )

            remix_edit = Task(
                description="Polish the remixed content. Fix phrasing, flow, and transitions. Strong opening and closing.",
                expected_output="Final polished remixed content.",
                agent=editor,
                context=[remix_write]
            )

            remix_crew = Crew(
                agents=[writer, editor],
                tasks=[remix_write, remix_edit],
                process=Process.sequential,
                verbose=False
            )

            try:
                result = str(remix_crew.kickoff())
                editor_out = str(remix_edit.output.raw) if remix_edit.output else result
                st.session_state["remix_output"] = editor_out
                st.session_state["remix_topic"] = selected["topic"]
                st.session_state["remix_format"] = new_format
                st.session_state["remix_tone"] = new_tone
                save_to_history(selected["topic"], new_format, new_tone, editor_out)
            except Exception as e:
                st.error(f"Remix failed: {str(e)[:200]}")

    if st.session_state.get("remix_output"):
        st.success("✦ Remix ready!")
        st.markdown('<div class="section-label" style="margin-top:1.5rem;">✦ Remixed Content</div>', unsafe_allow_html=True)

        # Stats
        txt = st.session_state["remix_output"]
        wc = len(txt.split())
        rt = max(1, round(wc / 200))
        st.markdown(f"""
        <div style="background:white; border:1px solid #e0dcff; border-radius:10px; padding:0.8rem 1.5rem; display:inline-flex; gap:2rem; margin-bottom:1rem;">
            <div style="text-align:center;"><div style="font-family:Syne,sans-serif; font-weight:800; color:#7c6af7;">{wc:,}</div><div style="font-size:0.7rem; color:#888; text-transform:uppercase;">Words</div></div>
            <div style="width:1px; background:#e0dcff;"></div>
            <div style="text-align:center;"><div style="font-family:Syne,sans-serif; font-weight:800; color:#7c6af7;">{rt} min</div><div style="font-size:0.7rem; color:#888; text-transform:uppercase;">Read Time</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div class="output-box">{txt}</div>', unsafe_allow_html=True)

        fname = st.session_state["remix_topic"][:30].replace(" ", "_").lower()
        fmt_slug = new_format.lower().replace(" ", "_")
        st.download_button(
            label="⬇ Download Remix",
            data=txt,
            file_name=f"{fname}_remix_{fmt_slug}.md",
            mime="text/markdown"
        )