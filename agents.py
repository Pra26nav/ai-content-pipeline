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

critic = Agent(
    role="Content Quality Critic",
    goal="Evaluate content quality and provide a structured score across multiple professional parameters",
    backstory="Expert content strategist with 15 years experience across SEO, journalism, and digital marketing. Provides brutally honest, data-driven content assessments.",
    llm="groq/llama-3.3-70b-versatile",
    verbose=True
)

"""
agents.py
Defines the 4 CrewAI agents used in the content pipeline.
- researcher: Real-time web search using SerperDev
- writer: Format-specific content generation
- editor: Polish and flow improvement
- critic: 6-parameter content scoring
"""
from crewai import Agent
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# Web search tool for real-time research
search_tool = SerperDevTool()

researcher = Agent(
    role="Research Specialist",
    goal="Find key facts, trends, and insights using live web search",
    backstory="Expert researcher who finds accurate, up-to-date information.",
    llm="groq/llama-3.1-8b-instant",
    tools=[search_tool],
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write engaging, format-specific content using research provided",
    backstory="Skilled writer who produces compelling content in any format.",
    llm="groq/llama-3.1-8b-instant",
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Polish content for flow, clarity, and professional tone",
    backstory="Seasoned editor with sharp eye for quality.",
    llm="groq/llama-3.1-8b-instant",
    verbose=True
)

critic = Agent(
    role="Content Quality Critic",
    goal="Score content on 6 professional parameters and output structured JSON",
    backstory="Expert content strategist providing data-driven assessments.",
    llm="groq/llama-3.1-8b-instant",
    verbose=True
)