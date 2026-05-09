import streamlit as st
from crewai import Crew, Process
from crewai import Task
from agents import researcher, writer, editor
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Content Pipeline",
    page_icon="✦",
    layout="centered"
)

# --- CUSTOM CSS ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;800&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #0a0a0f;
    color: #e8e6f0;
}

.stApp {
    background: linear-gradient(135deg, #0a0a0f 0%, #0f0f1a 50%, #0a0a0f 100%);
}

/* Header */
.hero {
    text-align: center;
    padding: 3rem 0 2rem 0;
    border-bottom: 1px solid #1e1e2e;
    margin-bottom: 2.5rem;
}
.hero h1 {
    font-family: 'Syne', sans-serif;
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, #e8e6f0, #7c6af7, #e8e6f0);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin: 0;
    letter-spacing: -1px;
}
.hero p {
    color: #6b6880;
    font-size: 0.95rem;
    margin-top: 0.5rem;
    font-weight: 300;
}

/* Section labels */
.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: #7c6af7;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #1e1e2e;
}

/* Card container */
.card {
    background: #111120;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* Inputs */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: #0d0d1a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    padding: 0.75rem 1rem !important;
    transition: border-color 0.2s !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #7c6af7 !important;
    box-shadow: 0 0 0 2px rgba(124,106,247,0.15) !important;
}
.stTextInput > div > div > input::placeholder,
.stTextArea > div > div > textarea::placeholder {
    color: #3a3a52 !important;
}

/* Labels */
.stTextInput label, .stTextArea label, .stSelectbox label, .stSlider label {
    color: #9896a8 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

/* Selectbox */
.stSelectbox > div > div {
    background: #0d0d1a !important;
    border: 1px solid #2a2a3e !important;
    border-radius: 10px !important;
    color: #e8e6f0 !important;
}

/* Slider */
.stSlider > div > div > div > div {
    background: #7c6af7 !important;
}

/* Button */
.stButton > button {
    background: linear-gradient(135deg, #7c6af7, #5b4fd4) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 2.5rem !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1px !important;
    width: 100% !important;
    transition: all 0.2s !important;
    margin-top: 0.5rem !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #8f7fff, #6c5fe0) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 25px rgba(124,106,247,0.35) !important;
}
.stButton > button:disabled {
    background: #1e1e2e !important;
    color: #3a3a52 !important;
}

/* Download button */
.stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #7c6af7 !important;
    color: #7c6af7 !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    width: 100% !important;
}

/* Output area */
.output-box {
    background: #0d0d1a;
    border: 1px solid #1e1e2e;
    border-radius: 16px;
    padding: 2rem;
    margin-top: 2rem;
    line-height: 1.8;
    color: #d4d2e0;
    font-size: 0.95rem;
}

/* Agent status badges */
.agent-badge {
    display: inline-block;
    background: #1a1a2e;
    border: 1px solid #2a2a3e;
    border-radius: 20px;
    padding: 0.3rem 0.8rem;
    font-size: 0.75rem;
    color: #7c6af7;
    margin-right: 0.5rem;
    font-family: 'DM Sans', sans-serif;
}

/* Divider */
hr {
    border: none;
    border-top: 1px solid #1e1e2e !important;
    margin: 2rem 0 !important;
}

/* Spinner */
.stSpinner > div {
    border-top-color: #7c6af7 !important;
}

/* Success */
.stSuccess {
    background: #0f1f0f !important;
    border: 1px solid #1a3a1a !important;
    border-radius: 10px !important;
    color: #4caf50 !important;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# --- HERO ---
st.markdown("""
<div class="hero">
    <h1>✦ AI Content Pipeline</h1>
    <p>Three autonomous agents. One publication-ready blog post.</p>
</div>
""", unsafe_allow_html=True)

# --- AGENT BADGES ---
st.markdown("""
<div style="text-align:center; margin-bottom:2rem;">
    <span class="agent-badge">🔍 Researcher</span>
    <span style="color:#3a3a52; margin-right:0.5rem;">→</span>
    <span class="agent-badge">✍️ Writer</span>
    <span style="color:#3a3a52; margin-right:0.5rem;">→</span>
    <span class="agent-badge">✨ Editor</span>
</div>
""", unsafe_allow_html=True)

# --- INPUTS ---
st.markdown('<div class="section-label">✦ Content Brief</div>', unsafe_allow_html=True)

topic = st.text_input(
    "Blog Topic *",
    placeholder="e.g. How AI Agents are changing software development"
)

keywords = st.text_input(
    "Focus Keywords",
    placeholder="e.g. LangChain, CrewAI, automation, LLM  (optional)"
)

references = st.text_area(
    "References / Context",
    placeholder="Paste URLs, notes, or specific points you want covered...  (optional)",
    height=120
)

st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.markdown('<div class="section-label">✦ Output Settings</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    output_format = st.selectbox(
        "Output Format",
        ["Blog Post", "LinkedIn Post", "Twitter Thread", "Email Newsletter"]
    )
with col2:
    tone = st.selectbox(
        "Writing Tone",
        ["Informative & Conversational", "Professional & Formal", "Casual & Friendly", "Technical & In-depth"]
    )
with col3:
    word_count = st.slider("Word Count", min_value=300, max_value=1500, value=700, step=100)

st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

run = st.button("✦ Generate Blog Post", disabled=not topic)

# --- GENERATION ---
if run and topic:
    with st.spinner("Agents working..."):

        enriched_topic = topic
        if keywords:
            enriched_topic += f"\n\nFocus keywords to include: {keywords}"
        if references:
            enriched_topic += f"\n\nReferences and context to consider:\n{references}"

        research_task = Task(
            description=f"""Research the topic: '{enriched_topic}'.
            Find: key concepts, current trends, interesting facts, and real-world examples.
            Output a structured research brief with bullet points.""",
            expected_output="Structured research brief with key facts, trends, and examples.",
            agent=researcher
        )
        # Format-specific instructions
        format_instructions = {
            "Blog Post": f"""Write a blog post about '{topic}'.
                Structure: catchy title, intro, 3-4 sections with subheadings, conclusion.
                Length: {word_count} words. Tone: {tone}.""",

            "LinkedIn Post": f"""Write a LinkedIn post about '{topic}'.
                Structure: strong hook line, 3-5 short punchy paragraphs, 1 insight or CTA at end.
                Max 300 words. No subheadings. Use line breaks for readability.
                Tone: {tone}. Add 5 relevant hashtags at the end.""",

            "Twitter Thread": f"""Write a Twitter/X thread about '{topic}'.
                Format: numbered tweets (1/, 2/, 3/ etc.), 15-20 tweets max.
                Each tweet max 280 chars. Start with a hook tweet. End with a summary tweet.
                Tone: {tone}. Make it punchy and shareable.""",

            "Email Newsletter": f"""Write an email newsletter about '{topic}'.
                Structure: subject line, greeting, intro hook, 3 key sections, CTA, sign-off.
                Length: {word_count} words. Tone: {tone}.
                Make it feel personal and valuable to the reader.""",
        }

        write_task = Task(
            description=f"Using the research brief: {format_instructions[output_format]}",
            expected_output=f"Complete {output_format} about the topic.",
            agent=writer,
            context=[research_task]
        )
        
        edit_task = Task(
            description="""Review and polish the blog post.
            Fix: awkward phrasing, repetition, weak transitions.
            Ensure: professional tone, smooth flow, strong opening and closing.
            Output the final, publication-ready blog post.""",
            expected_output="Final polished blog post ready to publish.",
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

    st.success("✦ Blog post ready")

    st.markdown(f'<div class="section-label" style="margin-top:2rem;">✦ {output_format}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="output-box">{final_text}</div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    fmt_slug = output_format.lower().replace(" ", "_")
    filename = topic[:40].replace(" ", "_").lower() + f"_{fmt_slug}.md"
    st.download_button(
        label="⬇ Download as Markdown",
        data=final_text,
        file_name=filename,
        mime="text/markdown"
    )