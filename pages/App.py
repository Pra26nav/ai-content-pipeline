import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from crewai import Crew, Process, Task
from agents import researcher, writer, editor, critic
from dotenv import load_dotenv
import json
import re
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
    <span style="color:#7c6af7; margin-right:0.5rem; opacity:0.5;">→</span>
    <span class="agent-badge">🎯 Critic</span>
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
    with st.spinner("Agents working... Researcher → Writer → Editor → Critic"):
        enriched_topic = topic
        if keywords:
            enriched_topic += f"\n\nFocus keywords: {keywords}"
        if references:
            enriched_topic += f"\n\nReferences:\n{references}"

        research_task = Task(
            description=f"Research the topic: '{enriched_topic}'. Find key concepts, current trends, interesting facts, and real-world examples. Output structured research brief with bullet points.",
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

        score_task = Task(
            description=f"""You are a professional content critic. Evaluate the final content strictly on these 6 parameters.
For each parameter give a score out of 100 and one sentence of feedback.

Parameters:
1. CLARITY — Is the writing clear, easy to follow, and jargon-free where needed?
2. ENGAGEMENT — Does it hook the reader and keep them reading?
3. SEO POTENTIAL — Are keywords used naturally? Good heading structure?
4. TONE MATCH — Does the tone match the requested style: {tone}?
5. STRUCTURE — Is it well-organized with proper intro, body, conclusion?
6. ORIGINALITY — Does it offer fresh perspective or unique insights?

Output ONLY this exact JSON format, nothing else:
{{
  "clarity": {{"score": 85, "feedback": "one sentence here"}},
  "engagement": {{"score": 78, "feedback": "one sentence here"}},
  "seo": {{"score": 72, "feedback": "one sentence here"}},
  "tone_match": {{"score": 90, "feedback": "one sentence here"}},
  "structure": {{"score": 88, "feedback": "one sentence here"}},
  "originality": {{"score": 70, "feedback": "one sentence here"}},
  "overall": 80
}}""",
            expected_output="JSON object with scores and feedback for each parameter.",
            agent=critic,
            context=[edit_task]
        )

        crew = Crew(
        agents=[researcher, writer, editor, critic],
        tasks=[research_task, write_task, edit_task, score_task],
        process=Process.sequential,
        verbose=False
        )

        result = crew.kickoff()
        full_output = str(result)

        # Get editor output directly from task
        editor_output = str(edit_task.output.raw) if edit_task.output else ""

        import time
        max_retries = 3
        for attempt in range(max_retries):
            try:
                result = crew.kickoff()
                break
            except Exception as e:
                if "tool_use_failed" in str(e) and attempt < max_retries - 1:
                    time.sleep(2)
                    continue
                else:
                    raise e
        full_output = str(result)

        # Extract JSON score from output
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

    save_to_history(topic, output_format, tone, final_text)
    st.session_state["selected_history"] = None
    st.success("✦ Content ready")

    # --- SCORE DISPLAY ---
    score_data = st.session_state.get("last_score")
    final_text = st.session_state.get("last_content", "")

    if score_data:
        st.markdown('<div class="section-label" style="margin-top:2rem;">✦ Content Score</div>', unsafe_allow_html=True)

        overall = score_data.get("overall", 0)
        if overall >= 85:
            score_color, score_label = "#22c55e", "Excellent"
        elif overall >= 70:
            score_color, score_label = "#7c6af7", "Good"
        elif overall >= 55:
            score_color, score_label = "#f59e0b", "Average"
        else:
            score_color, score_label = "#ef4444", "Needs Work"

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

        params = [
            ("clarity", "🎯 Clarity"),
            ("engagement", "⚡ Engagement"),
            ("seo", "🔍 SEO"),
            ("tone_match", "🎨 Tone Match"),
            ("structure", "📐 Structure"),
            ("originality", "💡 Originality"),
        ]

        cards_html = ""
        for key, label in params:
            if key in score_data:
                s = score_data[key]["score"]
                fb = score_data[key]["feedback"]
                bar_color = "#22c55e" if s >= 85 else "#7c6af7" if s >= 70 else "#f59e0b" if s >= 55 else "#ef4444"
                cards_html += f"""
                <div style="background:#f8f7ff; border-radius:10px; padding:0.8rem;">
                    <div style="font-size:0.75rem; font-weight:600; color:#444; margin-bottom:0.3rem;">{label}</div>
                    <div style="font-family:Syne,sans-serif; font-size:1.4rem; font-weight:800; color:{bar_color};">{s}</div>
                    <div style="height:4px; background:#e0dcff; border-radius:2px; margin:0.4rem 0;">
                        <div style="width:{s}%; height:100%; background:{bar_color}; border-radius:2px;"></div>
                    </div>
                    <div style="font-size:0.72rem; color:#666; line-height:1.4;">{fb}</div>
                </div>"""

        st.markdown(cards_html + "</div></div>", unsafe_allow_html=True)

        # --- KEYWORD RECOMMENDATIONS ---
        recs = []
        if score_data.get("seo", {}).get("score", 100) < 75:
            recs.append(("🔍 SEO", [
                f"Add '{topic.split()[0]} guide' or '{topic.split()[0]} tips' naturally in first paragraph",
                "Include a question-based subheading (e.g. 'What is...' or 'How to...')",
                "Add location or year qualifier if relevant (e.g. '2026', 'in India')"
            ]))
        if score_data.get("engagement", {}).get("score", 100) < 75:
            recs.append(("⚡ Engagement", [
                "Add power words: 'proven', 'essential', 'surprising', 'little-known'",
                "Start a sentence with 'Here's what most people miss about...'",
                "Add a statistic or data point in the first 100 words"
            ]))
        if score_data.get("clarity", {}).get("score", 100) < 75:
            recs.append(("🎯 Clarity", [
                "Break any paragraph longer than 4 lines into two",
                "Replace passive voice with active: 'AI agents do X' not 'X is done by AI agents'",
                "Add a one-line TL;DR summary at the top"
            ]))
        if score_data.get("originality", {}).get("score", 100) < 75:
            recs.append(("💡 Originality", [
                f"Add a personal take: 'What this means for {topic.split()[0]} practitioners is...'",
                "Include a contrarian point: 'But here's what the mainstream view gets wrong'",
                "Reference a specific recent event or example from 2025-2026"
            ]))
        if score_data.get("tone_match", {}).get("score", 100) < 75:
            recs.append(("🎨 Tone", [
                f"Rewrite the intro to better match '{tone}' style",
                "Check sentence length — short sentences = casual, longer = formal",
                "Remove hedge words like 'perhaps', 'maybe', 'it could be' for professional tone"
            ]))
        if score_data.get("structure", {}).get("score", 100) < 75:
            recs.append(("📐 Structure", [
                "Ensure each section has a clear subheading",
                "Add a bullet list or numbered list in at least one section",
                "Conclusion should restate the main insight, not just summarize"
            ]))

        st.markdown("""
        <div style="background:#f8f7ff; border:1px solid #e0dcff; border-radius:14px; padding:1.5rem 2rem; margin-top:1rem;">
            <div style="font-family:'Syne',sans-serif; font-size:0.7rem; font-weight:600; letter-spacing:3px; text-transform:uppercase; color:#7c6af7; margin-bottom:1rem;">✦ Keyword Recommendations</div>
        """, unsafe_allow_html=True)

        if not recs:
            st.markdown('<div style="text-align:center; padding:1rem; color:#22c55e; font-family:Syne,sans-serif; font-weight:600;">✦ Content is well-optimized! No critical keyword gaps found.</div>', unsafe_allow_html=True)
        else:
            for param, suggestions in recs:
                pills = "".join([f'<div style="background:white; border:1px solid #e0dcff; border-radius:8px; padding:0.5rem 0.8rem; margin-bottom:0.5rem; font-size:0.82rem; color:#444; line-height:1.5;">→ {s}</div>' for s in suggestions])
                st.markdown(f'<div style="margin-bottom:1rem;"><div style="font-size:0.78rem; font-weight:700; color:#7c6af7; margin-bottom:0.4rem;">{param}</div>{pills}</div>', unsafe_allow_html=True)

        st.markdown("</div>", unsafe_allow_html=True)

    # --- OUTPUT ---
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
    st.download_button(label="⬇ Download Past Run", data=entry["output"], file_name=entry["topic"][:30].replace(" ", "_").lower() + "_past.md", mime="text/markdown", key="dl_history")