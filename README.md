# AI Content Pipeline 🤖

Multi-agent blog post generator built with CrewAI + Groq (Llama 3.3 70B).

## Architecture
3 agents work sequentially:
- **Researcher** → gathers facts, trends, examples on any topic
- **Writer** → drafts structured 600-800 word blog post
- **Editor** → polishes for publication quality

## Tech Stack
- [CrewAI](https://crewai.com) — multi-agent orchestration
- [Groq](https://groq.com) — fast LLM inference (free tier)
- Python 3.13

## Setup
```bash
git clone https://github.com/Pra26nav/ai-content-pipeline
cd ai-content-pipeline
python -m venv venv
venv\Scripts\activate
pip install crewai crewai-tools langchain-groq python-dotenv litellm
```

Add `.env`:

## Run
```bash
python main.py
```
Enter any topic → get publication-ready blog post saved to `.txt`

## Sample Output
Topic: *"How AI Agents are changing software development"*
→ See `how_ai_agents_are_changing_software_development_blog.txt`