import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from crewai import Crew, Process, Task, Agent
from agents import researcher, writer, editor, critic, search_tool
from dotenv import load_dotenv
import json
import re
import time
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

st.set_page_config(page_title="AI Content Pipeline", page_icon="✦", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
@media (prefers-color-scheme: dark) {
    .stApp { background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0a0f 100%) !important; color: #e8e6f0 !important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { background: #0d0d1a !important; color: #e8e6f0 !important; }
    .stSelectbox > div > div { background: #0d0d1a !important; color: #e8e6f0 !important; }
    .output-box { background: #0d0d1a; color: #d4d2e0; }
    [data-testid="stSidebar"] { background: #0a0a14 !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] label { color: #e8e6f0 !important; }
}
@media (prefers-color-scheme: light) {
    .stApp { background: #f8f7ff !important; color: #1a1a2e !important; }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea { background: #ffffff !important; color: #1a1a2e !important; }
    .stSelectbox > div > div { background: #ffffff !important; color: #1a1a2e !important; }
    .output-box { background: #ffffff; color: #1a1a2e; }
    [data-testid="stSidebar"] { background: #f0eeff !important; }
    [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] div, [data-testid="stSidebar"] label { color: #1a1a2e !important; }
}
[data-testid="stSidebar"] { border-right: 4px solid #7c6af7 !important; padding-top: 1.5rem !important; }
[data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; opacity: 1 !important; background: #7c6af7 !important; border-radius: 50% !important; color: white !important; }
.hero { text-align: center; padding: 2.5rem 0 2rem 0; border-bottom: 1px solid #7c6af7; margin-bottom: 2rem; }
.hero h1 { font-family: 'Syne', sans-serif; font-size: 2.6rem; font-weight: 800; background: linear-gradient(90deg, #5b4fd4, #7c6af7, #a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0; letter-spacing: -1px; }
.hero p { font-size: 0.9rem; margin-top: 0.4rem; font-weight: 300; opacity: 0.55; }
.section-label { font-family: 'Syne', sans-serif; font-size: 0.68rem; font-weight: 600; letter-spacing: 3px; text-transform: uppercase; color: #7c6af7; margin-bottom: 1.2rem; display: flex; align-items: center; gap: 0.5rem; }
.section-label::after { content: ''; flex: 1; height: 1px; background: #7c6af7; opacity: 0.25; }
.stTextInput > div > div > input, .stTextArea > div > div > textarea { border: 1.5px solid #7c6af7 !important; border-radius: 10px !important; font-family: 'DM Sans', sans-serif !important; font-size: 0.9rem !important; padding: 0.75rem 1rem !important; }
.stTextInput > div > div > input:focus, .stTextArea > div > div > textarea:focus { border-color: #a78bfa !important; box-shadow: 0 0 0 2px rgba(124,106,247,0.2) !important; }
.stTextInput > div > div > input::placeholder, .stTextArea > div > div > textarea::placeholder { color: #9896a8 !important; opacity: 1 !important; }
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label { font-size: 0.82rem !important; font-weight: 500 !important; color: #7c6af7 !important; }
.stSelectbox > div > div { border: 1.5px solid #7c6af7 !important; border-radius: 10px !important; }
.stSlider > div > div > div > div { background: #7c6af7 !important; }
.stButton > button { background: linear-gradient(135deg, #7c6af7, #5b4fd4) !important; color: white !important; border: none !important; border-radius: 10px !important; padding: 0.75rem 2rem !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; font-size: 0.88rem !important; width: 100% !important; transition: all 0.2s !important; margin-top: 0.4rem !important; }
.stButton > button:hover { background: linear-gradient(135deg, #8f7fff, #6c5fe0) !important; transform: translateY(-1px) !important; box-shadow: 0 8px 20px rgba(124,106,247,0.35) !important; }
.stButton > button:disabled { opacity: 0.35 !important; cursor: not-allowed !important; }
.stDownloadButton > button { background: transparent !important; border: 2px solid #7c6af7 !important; color: #7c6af7 !important; border-radius: 10px !important; font-family: 'Syne', sans-serif !important; font-weight: 600 !important; width: 100% !important; }
.output-box { border: 1.5px solid #7c6af7; border-radius: 16px; padding: 2rem; margin-top: 1.5rem; line-height: 1.8; font-size: 0.95rem; }
.agent-badge { display: inline-block; border: 1px solid #7c6af7; border-radius: 20px; padding: 0.3rem 0.8rem; font-size: 0.75rem; color: #7c6af7; margin-right: 0.5rem; }
hr { border: none; border-top: 1px solid #7c6af7 !important; opacity: 0.25; margin: 2rem 0 !important; }
#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
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
    <p>Four autonomous agents. One publication-ready piece of content.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; margin-bottom:2rem;">
    <span class="agent-badge">🔍 Researcher</span>
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">✍️ Writer</span>
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">✨ Editor</span>
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">🎯 Critic</span>
</div>
""", unsafe_allow_html=True)

# --- INPUTS ---
st.markdown('<div class="section-label">✦ Content Brief</div>', unsafe_allow_html=True)

topic = st.text_input("Blog Topic *", placeholder="e.g. How AI Agents are changing software development")

# --- TOPIC SUGGESTION ENGINE ---
col_sug1, col_sug2 = st.columns([1, 5])
with col_sug1:
    suggest = st.button("💡 Suggest Topics")

if suggest:
    past_topics = [e["topic"] for e in load_history()[:10]]
    past_context = ", ".join(past_topics) if past_topics else "AI, technology, business"
    with st.spinner("Finding trending topics..."):
        suggester = Agent(
            role="Content Strategist",
            goal="Suggest 5 trending content topics",
            backstory="Expert content strategist who tracks trends.",
            llm="groq/llama-3.1-8b-instant",
            tools=[search_tool],
            verbose=False
        )
        suggest_task = Task(
            description=f'User writes about: {past_context}. Search trending topics. Output ONLY JSON: {{"topics": ["topic1","topic2","topic3","topic4","topic5"]}}',
            expected_output="JSON with 5 topics.",
            agent=suggester
        )
        try:
            suggest_result = str(Crew(agents=[suggester], tasks=[suggest_task], process=Process.sequential, verbose=False).kickoff())
            json_m = re.search(r'\{[\s\S]*?"topics"[\s\S]*?\}', suggest_result)
            if json_m:
                st.session_state["suggestions"] = json.loads(json_m.group()).get("topics", [])
        except Exception:
            st.session_state["suggestions"] = []
            st.error("Could not fetch suggestions. Try again.")

if st.session_state.get("suggestions"):
    st.markdown("**💡 Click a topic to use it:**")
    cols = st.columns(len(st.session_state["suggestions"]))
    for i, sug in enumerate(st.session_state["suggestions"]):
        with cols[i]:
            if st.button(f"{sug[:35]}..." if len(sug) > 35 else sug, key=f"sug_{i}"):
                st.session_state["selected_topic"] = sug
                st.session_state["suggestions"] = []
                st.rerun()

if st.session_state.get("selected_topic"):
    topic = st.session_state["selected_topic"]

keywords = st.text_input("Focus Keywords", placeholder="e.g. LangChain, CrewAI, automation, LLM  (optional)")
references = st.text_area("References / Context", placeholder="Paste URLs, notes, or specific points you want covered...  (optional)", height=100)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">✦ Output Settings</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
with col1:
    output_format = st.selectbox("Output Format", ["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"])
with col2:
    tone = st.selectbox("Writing Tone", ["Informative & Conversational", "Professional & Formal", "Casual & Friendly", "Technical & In-depth"])
with col3:
    word_count = st.slider("Word Count", min_value=300, max_value=1500, value=700, step=100)
with col4:
    use_search = st.checkbox("🔍 Live Web Search", value=True, help="Disable to save tokens")

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
run = st.button("✦ Generate Content", disabled=not topic)

# --- GENERATION ---
if run and topic:
    with st.spinner("Agents working... Researcher → Writer → Editor → Critic"):
        enriched_topic = topic
        if keywords:
            enriched_topic += f". Keywords: {keywords}"
        if references:
            enriched_topic += f". Context: {references[:300]}"

        active_researcher = Agent(
            role="Research Specialist",
            goal="Find key facts and insights about the given topic",
            backstory="Expert researcher who finds accurate, relevant information.",
            llm="groq/llama-3.1-8b-instant",
            tools=[search_tool] if use_search else [],
            verbose=False,
            max_iter=2
        )

        research_task = Task(
            description=f"Research '{enriched_topic}'. Output bullet-point brief with key concepts, trends, facts.",
            expected_output="Structured research brief.",
            agent=active_researcher
        )

        format_instructions = {
            "Blog Post": f"Blog post about '{topic}'. Title, intro, 3-4 sections, conclusion. STRICT: {word_count} words max. Tone: {tone}.",
            "LinkedIn Post": f"LinkedIn post about '{topic}'. Hook, 3-5 paragraphs, CTA, 5 hashtags. Max 300 words. Tone: {tone}.",
            "Twitter Thread": f"Twitter thread about '{topic}'. 1/ to 15/ numbered tweets, max 280 chars each. Tone: {tone}.",
            "Email Newsletter": f"Email newsletter about '{topic}'. Subject, greeting, 3 sections, CTA, sign-off. STRICT: {word_count} words max. Tone: {tone}.",
        }

        write_task = Task(
            description=f"Using research: {format_instructions[output_format]}",
            expected_output=f"Complete {output_format}.",
            agent=writer,
            context=[research_task]
        )

        edit_task = Task(
            description="Polish content. Fix phrasing, flow, transitions. Keep same length.",
            expected_output="Final polished content.",
            agent=editor,
            context=[write_task]
        )

        score_task = Task(
            description=f'Score on 6 params. Output ONLY JSON: {{"clarity":{{"score":85,"feedback":"sentence"}},"engagement":{{"score":78,"feedback":"sentence"}},"seo":{{"score":72,"feedback":"sentence"}},"tone_match":{{"score":90,"feedback":"sentence"}},"structure":{{"score":88,"feedback":"sentence"}},"originality":{{"score":70,"feedback":"sentence"}},"overall":80}} Requested tone: {tone}.',
            expected_output="JSON scores.",
            agent=critic,
            context=[edit_task]
        )

        crew = Crew(
            agents=[active_researcher, writer, editor, critic],
            tasks=[research_task, write_task, edit_task, score_task],
            process=Process.sequential,
            verbose=False
        )

        max_retries = 3
        result = None
        for attempt in range(max_retries):
            try:
                result = crew.kickoff()
                break
            except Exception as e:
                err = str(e)
                if "rate_limit_exceeded" in err and attempt < max_retries - 1:
                    st.warning(f"Rate limit. Waiting 30s... (retry {attempt+2}/{max_retries})")
                    time.sleep(30)
                elif "tool_use_failed" in err and attempt < max_retries - 1:
                    time.sleep(3)
                else:
                    raise e

        full_output = str(result)
        editor_output = str(edit_task.output.raw) if edit_task.output else ""

        score_data = None
        json_match = re.search(r'\{[\s\S]*?"overall"[\s\S]*?\}', full_output)
        if json_match:
            try:
                score_data = json.loads(json_match.group())
                final_text = editor_output if editor_output else full_output[:json_match.start()].strip()
                if not final_text:
                    final_text = full_output
            except Exception:
                final_text = editor_output if editor_output else full_output
                score_data = None
        else:
            final_text = editor_output if editor_output else full_output
            score_data = None

        st.session_state["last_score"] = score_data
        st.session_state["last_content"] = final_text
        st.session_state["edit_mode"] = False
        st.session_state["edited_content"] = final_text

    save_to_history(topic, output_format, tone, final_text)
    st.session_state["selected_history"] = None
    st.success("✦ Content ready")

    score_data = st.session_state.get("last_score")
    final_text = st.session_state.get("last_content", "")

    # --- SCORE ---
    if score_data:
        st.markdown('<div class="section-label" style="margin-top:2rem;">✦ Content Score</div>', unsafe_allow_html=True)
        overall = score_data.get("overall", 0)
        if overall >= 85: score_color, score_label = "#22c55e", "Excellent"
        elif overall >= 70: score_color, score_label = "#7c6af7", "Good"
        elif overall >= 55: score_color, score_label = "#f59e0b", "Average"
        else: score_color, score_label = "#ef4444", "Needs Work"

        st.markdown(f"""
        <div style="background:white; border:2px solid {score_color}; border-radius:16px; padding:1.5rem 2rem; margin-bottom:1.5rem;">
            <div style="display:flex; align-items:center; gap:1.5rem; margin-bottom:1.5rem;">
                <div style="text-align:center;">
                    <div style="font-family:Syne,sans-serif; font-size:3rem; font-weight:800; color:{score_color}; line-height:1;">{overall}</div>
                    <div style="font-size:0.75rem; font-weight:600; text-transform:uppercase; letter-spacing:2px; color:{score_color};">{score_label}</div>
                </div>
                <div style="flex:1; height:8px; background:#f0eeff; border-radius:4px;">
                    <div style="width:{overall}%; height:100%; background:{score_color}; border-radius:4px;"></div>
                </div>
            </div>
            <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:1rem;">
        """, unsafe_allow_html=True)

        params = [("clarity","🎯 Clarity"),("engagement","⚡ Engagement"),("seo","🔍 SEO"),("tone_match","🎨 Tone Match"),("structure","📐 Structure"),("originality","💡 Originality")]
        cards_html = ""
        for key, label in params:
            if key in score_data:
                s = score_data[key]["score"]
                fb = score_data[key]["feedback"]
                bc = "#22c55e" if s >= 85 else "#7c6af7" if s >= 70 else "#f59e0b" if s >= 55 else "#ef4444"
                cards_html += f'<div style="background:#f8f7ff; border-radius:10px; padding:0.8rem;"><div style="font-size:0.75rem; font-weight:600; color:#444; margin-bottom:0.3rem;">{label}</div><div style="font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:{bc};">{s}</div><div style="height:4px; background:#e0dcff; border-radius:2px; margin:0.4rem 0;"><div style="width:{s}%; height:100%; background:{bc}; border-radius:2px;"></div></div><div style="font-size:0.72rem; color:#666; line-height:1.4;">{fb}</div></div>'
        st.markdown(cards_html + "</div></div>", unsafe_allow_html=True)

        # Keyword recs
        recs = []
        if score_data.get("seo", {}).get("score", 100) < 75:
            recs.append(("🔍 SEO", [f"Add '{topic.split()[0]} guide' in first paragraph", "Add question subheading (What is.../How to...)", "Add year/location qualifier (2026, in India)"]))
        if score_data.get("engagement", {}).get("score", 100) < 75:
            recs.append(("⚡ Engagement", ["Use power words: proven, essential, surprising", "Open with 'Here's what most people miss...'", "Add stat in first 100 words"]))
        if score_data.get("clarity", {}).get("score", 100) < 75:
            recs.append(("🎯 Clarity", ["Break paragraphs over 4 lines", "Use active voice", "Add TL;DR at top"]))
        if score_data.get("originality", {}).get("score", 100) < 75:
            recs.append(("💡 Originality", [f"Add: 'What this means for {topic.split()[0]} practitioners...'", "Include contrarian point", "Reference 2025-2026 example"]))
        if score_data.get("tone_match", {}).get("score", 100) < 75:
            recs.append(("🎨 Tone", [f"Rewrite intro for '{tone}' style", "Short sentences=casual, long=formal", "Remove hedge words: perhaps, maybe"]))
        if score_data.get("structure", {}).get("score", 100) < 75:
            recs.append(("📐 Structure", ["Each section needs subheading", "Add bullet/numbered list", "Conclusion: restate insight"]))

        st.markdown('<div style="background:#f8f7ff; border:1px solid #e0dcff; border-radius:14px; padding:1.5rem 2rem; margin-top:1rem;"><div style="font-family:Syne,sans-serif; font-size:0.7rem; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#7c6af7; margin-bottom:1rem;">✦ Keyword Recommendations</div>', unsafe_allow_html=True)
        if not recs:
            st.markdown('<div style="text-align:center; padding:1rem; color:#22c55e; font-family:Syne,sans-serif; font-weight:600;">✦ Content is well-optimized!</div>', unsafe_allow_html=True)
        else:
            for param, suggestions in recs:
                pills = "".join([f'<div style="background:white; border:1px solid #e0dcff; border-radius:8px; padding:0.5rem 0.8rem; margin-bottom:0.5rem; font-size:0.82rem; color:#444;">→ {s}</div>' for s in suggestions])
                st.markdown(f'<div style="margin-bottom:1rem;"><div style="font-size:0.78rem; font-weight:700; color:#7c6af7; margin-bottom:0.4rem;">{param}</div>{pills}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # --- READING STATS ---
    wc_actual = len(final_text.split())
    cc = len(final_text)
    rt = max(1, round(wc_actual / 200))
    if output_format == "Twitter Thread":
        tweets = [t.strip() for t in final_text.split('\n') if t.strip() and '/' in t[:4]]
        tweet_count = len(tweets)
        over_limit = [t for t in tweets if len(t) > 280]
        extra = f"<div style='text-align:center;'><div style='font-family:Syne,sans-serif; font-size:1.2rem; font-weight:800; color:#7c6af7;'>{tweet_count}</div><div style='font-size:0.7rem; color:#888; text-transform:uppercase;'>Tweets</div></div>"
        if over_limit:
            extra += f"<div style='text-align:center;'><div style='font-family:Syne,sans-serif; font-size:1.2rem; font-weight:800; color:#ef4444;'>{len(over_limit)}</div><div style='font-size:0.7rem; color:#888; text-transform:uppercase;'>Over 280</div></div>"
    else:
        extra = f"<div style='text-align:center;'><div style='font-family:Syne,sans-serif; font-size:1.2rem; font-weight:800; color:#7c6af7;'>{rt} min</div><div style='font-size:0.7rem; color:#888; text-transform:uppercase;'>Read Time</div></div>"

    st.markdown(f"""
    <div style="display:flex; gap:1rem; margin:1.5rem 0 1rem 0;">
        <div style="background:white; border:1px solid #e0dcff; border-radius:12px; padding:0.8rem 1.5rem; display:flex; gap:2rem; align-items:center; flex:1;">
            <div style="text-align:center;"><div style="font-family:Syne,sans-serif; font-size:1.2rem; font-weight:800; color:#7c6af7;">{wc_actual:,}</div><div style="font-size:0.7rem; color:#888; text-transform:uppercase; letter-spacing:1px;">Words</div></div>
            <div style="width:1px; background:#e0dcff; height:2rem;"></div>
            <div style="text-align:center;"><div style="font-family:Syne,sans-serif; font-size:1.2rem; font-weight:800; color:#7c6af7;">{cc:,}</div><div style="font-size:0.7rem; color:#888; text-transform:uppercase; letter-spacing:1px;">Characters</div></div>
            <div style="width:1px; background:#e0dcff; height:2rem;"></div>
            {extra}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- OUTPUT + EDIT ---
    st.markdown(f'<div class="section-label" style="margin-top:2rem;">✦ {output_format}</div>', unsafe_allow_html=True)
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = False

    col_view, col_edit = st.columns([6, 1])
    with col_edit:
        if st.button("✏️ Edit" if not st.session_state["edit_mode"] else "👁 View"):
            st.session_state["edit_mode"] = not st.session_state["edit_mode"]
            st.rerun()

    if st.session_state["edit_mode"]:
        edited = st.text_area("Edit your content:", value=st.session_state.get("edited_content", final_text), height=500, key="content_editor")
        st.session_state["edited_content"] = edited
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✦ Save Changes"):
                st.session_state["edit_mode"] = False
                st.success("Saved!")
                st.rerun()
        with c2:
            if st.button("↺ Reset to Original"):
                st.session_state["edited_content"] = final_text
                st.success("Reset.")
                st.rerun()
    else:
        display_text = st.session_state.get("edited_content", final_text)
        st.markdown(f'<div class="output-box">{display_text}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    download_text = st.session_state.get("edited_content", final_text)
    fmt_slug = output_format.lower().replace(" ", "_")
    filename = topic[:40].replace(" ", "_").lower() + f"_{fmt_slug}.md"

    col_dl1, col_dl2 = st.columns(2)
    with col_dl1:
        st.download_button(label="⬇ Download as Markdown", data=download_text, file_name=filename, mime="text/markdown")
    with col_dl2:
        try:
            from fpdf import FPDF
            import unicodedata
            def clean_pdf(text):
                return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(20, 20, 20)
            pdf.set_font("Helvetica", "B", 16)
            pdf.set_text_color(124, 106, 247)
            pdf.cell(0, 10, "AI Content Pipeline", ln=True)
            pdf.set_font("Helvetica", "", 9)
            pdf.set_text_color(150, 150, 150)
            pdf.cell(0, 6, clean_pdf(f"Format: {output_format}  |  Tone: {tone}  |  {datetime.now().strftime('%d %b %Y')}"), ln=True)
            pdf.ln(4)
            pdf.set_draw_color(124, 106, 247)
            pdf.set_line_width(0.5)
            pdf.line(20, pdf.get_y(), 190, pdf.get_y())
            pdf.ln(6)
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(30, 30, 30)
            for line in download_text.split('\n'):
                line = clean_pdf(line.strip())
                if not line:
                    pdf.ln(3)
                    continue
                if line.startswith('# '):
                    pdf.set_font("Helvetica", "B", 14); pdf.set_text_color(30, 30, 46)
                    pdf.multi_cell(0, 8, line[2:])
                    pdf.set_font("Helvetica", "", 11); pdf.set_text_color(30, 30, 30)
                elif line.startswith('## '):
                    pdf.set_font("Helvetica", "B", 12); pdf.set_text_color(124, 106, 247)
                    pdf.multi_cell(0, 7, line[3:])
                    pdf.set_font("Helvetica", "", 11); pdf.set_text_color(30, 30, 30)
                elif line.startswith('### '):
                    pdf.set_font("Helvetica", "B", 11)
                    pdf.multi_cell(0, 7, line[4:])
                    pdf.set_font("Helvetica", "", 11)
                elif line.startswith('- ') or line.startswith('* '):
                    pdf.multi_cell(0, 6, f"  - {line[2:]}")
                else:
                    pdf.multi_cell(0, 6, line)
                pdf.ln(1)
            pdf.set_y(-20)
            pdf.set_font("Helvetica", "I", 8)
            pdf.set_text_color(180, 180, 180)
            pdf.cell(0, 10, "Generated by AI Content Pipeline | github.com/Pra26nav/ai-content-pipeline", align="C")
            pdf_bytes = pdf.output()
            st.download_button(label="⬇ Download as PDF", data=bytes(pdf_bytes), file_name=filename.replace('.md', '.pdf'), mime="application/pdf", key="pdf_dl")
        except Exception as ex:
            st.error(f"PDF error: {str(ex)[:100]}")

# --- HISTORY VIEWER ---
if st.session_state.get("selected_history"):
    entry = st.session_state["selected_history"]
    st.markdown("---")
    st.markdown(f'<div class="section-label">✦ Past Run — {entry["timestamp"]}</div>', unsafe_allow_html=True)
    st.markdown(f"**Topic:** {entry['topic']} &nbsp;|&nbsp; **Format:** {entry['format']} &nbsp;|&nbsp; **Tone:** {entry['tone']}", unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{entry["output"]}</div>', unsafe_allow_html=True)
    st.download_button(label="⬇ Download Past Run", data=entry["output"], file_name=entry["topic"][:30].replace(" ", "_").lower() + "_past.md", mime="text/markdown", key="dl_history")