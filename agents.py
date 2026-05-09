from crewai import Agent
from dotenv import load_dotenv

load_dotenv()

# CrewAI 1.x — pass LLM as string "provider/model"
researcher = Agent(
    role="Research Specialist",
    goal="Find key facts, trends, and insights about the given topic",
    backstory="Expert researcher who digs deep into topics and extracts the most relevant, accurate information.",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write an engaging, well-structured blog post using the research provided",
    backstory="Skilled writer who turns raw research into compelling blog content with clear structure.",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Polish the blog post — fix flow, clarity, tone, and ensure it reads professionally",
    backstory="Seasoned editor with sharp eye for quality. Makes good content great.",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)