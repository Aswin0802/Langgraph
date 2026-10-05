
import os
import psycopg

from pathlib import Path
from dotenv import load_dotenv
from psycopg.rows import dict_row

from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.postgres import PostgresSaver
from langchain.chat_models import init_chat_model
from langchain_core.messages import BaseMessage

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

model = init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0.4
)

def chat_message(state: ChatState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

DB_URI = "postgresql://postgres:Aswin%402004@localhost:5432/langgraph?sslmode=disable"
if not DB_URI:
    raise ValueError("DB_URI is missing from your .env file")

conn = psycopg.connect(
    DB_URI,
    autocommit=True,
    row_factory=dict_row
)

checkpointer = PostgresSaver(conn)
checkpointer.setup()

graph = StateGraph(ChatState)
graph.add_node("chat_message", chat_message)
graph.add_edge(START, "chat_message")
graph.add_edge("chat_message", END)

workflow = graph.compile(checkpointer=checkpointer)

def get_all_threads():
    threads = set()

    for checkpoint in checkpointer.list(None):
        thread_id = checkpoint.config["configurable"].get("thread_id")
        if thread_id:
            threads.add(thread_id)

    return list(threads)
