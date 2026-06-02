"""
Entry point for running the AI agent with a user query.
Loads environment variables, sets up the database, and executes the agent.
"""
from dotenv import load_dotenv

load_dotenv()

from agent import agent  # noqa: E402
from database import setup_database  # noqa: E402
from haystack.dataclasses import ChatMessage  # noqa: E402

setup_database()

user_query = "What is the most common disease among our smoker patients?"

messages = [ChatMessage.from_user(user_query)]

print("⌛ Running the agent...")
agent_result = agent.run(messages=messages)

print("\n🤖:", agent_result["last_message"].text)
