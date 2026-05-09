from crewai import Crew, Process
from agents import researcher, writer, editor
from tasks import create_tasks
from dotenv import load_dotenv

load_dotenv()

def run_pipeline(topic: str):
    print(f"\n🚀 Starting content pipeline for: '{topic}'\n")
    print("=" * 50)

    tasks = create_tasks(topic)

    crew = Crew(
        agents=[researcher, writer, editor],
        tasks=tasks,
        process=Process.sequential,  # Researcher → Writer → Editor in order
        verbose=True
    )

    result = crew.kickoff()

    print("\n" + "=" * 50)
    print("✅ FINAL BLOG POST:")
    print("=" * 50)
    print(result)

    # Save to file
    filename = topic.replace(" ", "_").lower() + "_blog.txt"
    with open(filename, "w") as f:
        f.write(str(result))
    print(f"\n📄 Saved to: {filename}")

if __name__ == "__main__":
    topic = input("Enter blog topic: ")
    run_pipeline(topic)