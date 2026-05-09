from crewai import Task
from agents import researcher, writer, editor

def create_tasks(topic: str):

    research_task = Task(
        description=f"""Research the topic: '{topic}'.
        Find: key concepts, current trends, interesting facts, and real-world examples.
        Output a structured research brief with bullet points.""",
        expected_output="Structured research brief with key facts, trends, and examples.",
        agent=researcher
    )

    write_task = Task(
        description=f"""Using the research brief, write a blog post about '{topic}'.
        Structure: catchy title, intro, 3-4 sections with subheadings, conclusion.
        Length: 600-800 words. Tone: informative but conversational.""",
        expected_output="Complete blog post with title, sections, and conclusion.",
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

    return [research_task, write_task, edit_task]