from crewai import Agent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# Web search tool — researcher will google in real time
search_tool = SerperDevTool()

researcher = Agent(
    role="Research Specialist",
    goal="Find the most current, accurate facts, trends, and insights about the given topic using web search",
    backstory="Expert researcher who searches the web to find real, up-to-date information. Never relies on old knowledge — always verifies with live search results.",
    llm="groq/llama-3.3-70b-versatile",
    tools=[search_tool],  # WEB SEARCH ENABLED
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