import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import streamlit as st
from crewai import Crew, Process
from crewai import Task
from agents import researcher, writer, editor
from dotenv import load_dotenv
import json
import os
from datetime import datetime

load_dotenv()

HISTORY_FILE = "history.json"

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
        "topic": topic,
        "format": output_format,
        "tone": tone,
        "output": result_text
    }
    history.insert(0, entry)
    history = history[:20]
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
    return entry

st.set_page_config(
    page_title="AI Content Pipeline",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SINGLE CLEAN CSS BLOCK ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* ── DARK MODE ── */
@media (prefers-color-scheme: dark) {
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0a0f 100%) !important; color: #e8e6f0 !important; }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea { background: #0d0d1a !important; color: #e8e6f0 !important; }
    .stSelectbox > div > div { background: #0d0d1a !important; color: #e8e6f0 !important; }
    .output-box { background: #0d0d1a; color: #d4d2e0; }
    [data-testid="stSidebar"] { background: #0a0a14 !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #e8e6f0 !important; }
}

/* ── LIGHT MODE ── */
@media (prefers-color-scheme: light) {
    .stApp { background: #f8f7ff !important; color: #1a1a2e !important; }
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea { background: #ffffff !important; color: #1a1a2e !important; }
    .stSelectbox > div > div { background: #ffffff !important; color: #1a1a2e !important; }
    .output-box { background: #ffffff; color: #1a1a2e; }
    [data-testid="stSidebar"] { background: #f0eeff !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div,
    [data-testid="stSidebar"] label { color: #1a1a2e !important; }
}

/* ── SIDEBAR BORDER — thick purple, always visible ── */
[data-testid="stSidebar"] {
    border-right: 4px solid #7c6af7 !important;
    padding-top: 1.5rem !important;
}

/* Sidebar collapse toggle — force visible */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    background: #7c6af7 !important;
    border-radius: 50% !important;
    color: white !important;
}

/* ── HERO ── */
.hero { text-align: center; padding: 2.5rem 0 2rem 0; border-bottom: 1px solid #7c6af7; margin-bottom: 2rem; }
.hero h1 { font-family: 'Syne', sans-serif; font-size: 2.6rem; font-weight: 800; background: linear-gradient(90deg, #5b4fd4, #7c6af7, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; }
.hero p { font-size: 0.9rem; margin-top: 0.4rem; font-weight: 300; opacity: 0.55; }

/* ── SECTION LABELS ── */
.section-label { font-family: 'Syne', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: #7c6af7; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #7c6af7; opacity: 0.25; }

/* ── INPUTS ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    border: 1.5px solid #7c6af7 !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #a78bfa !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important;
}

/* Placeholder — clearly readable */
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #9896a8 !important;
    opacity: 1 !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    font-size: 0.82rem !important; font-weight: 500 !important; color: #7c6af7 !important;
}

/* Selectbox */
.stSelectbox > div > div { border: 1.5px solid #7c6af7 !important; border-radius: 10px !important; }

/* Slider */
.stSlider > div > div > div > div { background: #7c6af7 !important; }

/* ── BUTTONS ── */
.stButton > button {
    background: linear-gradient(135deg, #7c6af7, #5b4fd4) !important;
    color: white !important; border: none !important; border-radius: 10px !important;
    padding: 0.75rem 2rem !important; font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important; font-size: 0.88rem !important; width: 100% !important;
    transition: all 0.2s !important; margin-top: 0.4rem !important;
}
.stButton > button:hover { background: linear-gradient(135deg, #8f7fff, #6c5fe0) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 20px rgba(124,106,247,0.35) !important; }
.stButton > button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }

/* Download */
.stDownloadButton > button { background: transparent !important; border: 2px solid #7c6af7 !important; color: #7c6af7 !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; width: 100% !important; }

/* ── OUTPUT BOX ── */
.output-box { border: 1.5px solid #7c6af7; border-radius: 16px; padding: 2rem; margin-top: 1.5rem; line-height: 1.8; font-size: 0.95rem; }

/* ── AGENT BADGES ── */
.agent-badge { display: inline-block; border: 1px solid #7c6af7; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.75rem; color: #7c6af7; margin-right: 0.5rem; }

/* ── MISC ── */
hr { border: none; border-top: 1px solid #7c6af7 !important; opacity: 0.25; margin: 2rem 0 !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR HISTORY ---
with st.sidebar:
    st.markdown("## 🕘 History")
    st.markdown("---")
    history = load_history()

    if not history:
        st.info("No runs yet.\nGenerate content to see history here.")
    else:
        for entry in history:
            with st.expander(f"📄 {entry['topic'][:32]}"):
                st.markdown(f"🕐 {entry['timestamp']}")
                st.markdown(f"📋 **{entry['format']}** · {entry['tone'][:20]}")
                if st.button("Load this →", key=f"load_{entry['id']}"):
                    st.session_state["selected_history"] = entry
                    st.rerun()

# --- HERO ---
st.markdown("""
<div class="hero">
    <h1>✦ AI Content Pipeline</h1>
    <p>Three autonomous agents. One publication-ready piece of content.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:2rem;">
    <span class="agent-badge">🔍 Researcher</span>
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">✍️ Writer</span>
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">✨ Editor</span>
</div>
""", unsafe_allow_html=True)

# --- INPUTS ---
st.markdown('<div class="section-label">✦ Content Brief</div>', unsafe_allow_html=True)

topic = st.text_input("Blog Topic *", placeholder="e.g. How AI Agents are changing software development")
keywords = st.text_input("Focus Keywords", placeholder="e.g. LangChain, CrewAI, automation, LLM  (optional)")
references = st.text_area("References / Context", placeholder="Paste URLs, notes, or specific points you want covered...  (optional)", height=120)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">✦ Output Settings</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    output_format = st.selectbox("Output Format", ["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"])
with col2:
    tone = st.selectbox("Writing Tone", ["Informative & Conversational", "Professional & Formal", "Casual & Friendly", "Technical & In-depth"])
with col3:
    word_count = st.slider("Word Count", min_value=300, max_value=1500, value=700, step=100)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
run = st.button("✦ Generate Content", disabled=not topic)

# --- GENERATION ---
if run and topic:
    with st.spinner("Agents working... Researcher → Writer → Editor"):
        enriched_topic = topic
        if keywords:
            enriched_topic += f"\n\nFocus keywords: {keywords}"
        if references:
            enriched_topic += f"\n\nReferences:\n{references}"

        research_task = Task(
            description=f"""Research the topic: '{enriched_topic}'.
            Find: key concepts, current trends, interesting facts, and real-world examples.
            Output a structured research brief with bullet points.""",
            expected_output="Structured research brief.",
            agent=researcher
        )

        format_instructions = {
            "Blog Post": f"Write a blog post about '{topic}'. Structure: catchy title, intro, 3-4 sections with subheadings, conclusion. Length: {word_count} words. Tone: {tone}.",
            "LinkedIn Post": f"Write a LinkedIn post about '{topic}'. Strong hook, 3-5 short paragraphs, CTA. Max 300 words. Tone: {tone}. Add 5 hashtags.",
            "Twitter Thread": f"Write a Twitter/X thread about '{topic}'. Numbered tweets (1/, 2/ etc.), 15-20 tweets, max 280 chars each. Hook tweet first. Tone: {tone}.",
            "Email Newsletter": f"Write an email newsletter about '{topic}'. Subject line, greeting, intro, 3 sections, CTA, sign-off. Length: {word_count} words. Tone: {tone}.",
        }

        write_task = Task(
            description=f"Using the research brief: {format_instructions[output_format]}",
            expected_output=f"Complete {output_format}.",
            agent=writer,
            context=[research_task]
        )

        edit_task = Task(
            description="Polish the content. Fix phrasing, repetition, weak transitions. Strong opening and closing.",
            expected_output="Final publication-ready content.",
            agent=editor,
            context=[write_task]
        )

        crew = Crew(
            agents=[researcher, writer, editor],
            tasks=[research_task, write_task, edit_task],
            process=Process.sequential,
            verbose=False
        )

        result = crew.kickoff()
        final_text = str(result)

    save_to_history(topic, output_format, tone, final_text)
    st.session_state["selected_history"] = None

    st.success("✦ Content ready")
    st.markdown(f'<div class="section-label" style="margin-top:2rem;">✦ {output_format}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{final_text}</div>', unsafe_allow_html=True)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    fmt_slug = output_format.lower().replace(" ", "_")
    filename = topic[:40].replace(" ", "_").lower() + f"_{fmt_slug}.md"
    st.download_button(label="⬇ Download as Markdown", data=final_text, file_name=filename, mime="text/markdown")

# --- HISTORY VIEWER ---
if st.session_state.get("selected_history"):
    entry = st.session_state["selected_history"]
    st.markdown("---")
    st.markdown(f'<div class="section-label">✦ Past Run — {entry["timestamp"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**Topic:** {entry['topic']} &nbsp;|&nbsp; **Format:** {entry['format']} &nbsp;|&nbsp; **Tone:** {entry['tone']}", unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{entry["output"]}</div>', unsafe_allow_html=True)
    st.download_button(
        label="⬇ Download Past Run",
        data=entry["output"],
        file_name=entry["topic"][:30].replace(" ", "_").lower() + "_past.md",
        mime="text/markdown",
        key="dl_history"
    )