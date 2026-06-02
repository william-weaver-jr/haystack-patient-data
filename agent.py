"""
Assembles the AI agent using the defined tools and system prompt.
The agent configuration — model choice, tools, and state schema — is managed here.
"""
from haystack.components.agents import Agent
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.generators.utils import print_streaming_chunk
from haystack.dataclasses import Document

from prompts import agent_prompt
from tools import get_patient_information, search_tool

agent = Agent(
    chat_generator=OpenAIChatGenerator(model="gpt-4o-mini"),
    system_prompt=agent_prompt,
    tools=[search_tool, get_patient_information],
    state_schema={"documents": {"type": list[Document]}},
    streaming_callback=print_streaming_chunk
)
