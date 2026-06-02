"""
Defines the tools available to the AI agent: a natural language SQL query tool and a web search tool.
Adding, removing, or modifying agent capabilities should be done here.
"""
from typing import Annotated

from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.components.generators.chat import OpenAIChatGenerator
from haystack.components.websearch import SerperDevWebSearch
from haystack.dataclasses import ChatMessage
from haystack.tools import ComponentTool, tool

from database import SQLConnector
from prompts import query_to_sql_prompt


def _doc_to_string(documents) -> str:
    result_str = ""
    for document in documents:
        result_str += f"Content for {document.meta['link']}: {document.content}\n\n"
    return result_str


search_tool = ComponentTool(
    component=SerperDevWebSearch(top_k=5),
    name="web_search_tool",
    description="Search the web",
    outputs_to_string={"source": "documents", "handler": _doc_to_string},
    outputs_to_state={"documents": {"source": "documents"}}
)

sql_pipeline = Pipeline()
sql_pipeline.add_component(
    "prompt_builder",
    ChatPromptBuilder(template=[ChatMessage.from_user(query_to_sql_prompt)], required_variables="*")
)
sql_pipeline.add_component("chat_generator", OpenAIChatGenerator(model="gpt-4o-mini"))
sql_pipeline.add_component("sql_connector", SQLConnector("patient_data.db"))

sql_pipeline.connect("prompt_builder.prompt", "chat_generator.messages")
sql_pipeline.connect("chat_generator.replies", "sql_connector.llm_replies")


@tool
def get_patient_information(
    query: Annotated[str, "Natural language query to fetch data from an SQL database"],
) -> str:
    """
    Get patient information from the SQL database with natural language queries
    """
    results = sql_pipeline.run({"prompt_builder": {"query": query}})
    return results["sql_connector"]["results"][0]
