from langgraph.graph import StateGraph,START,END
from langgraph.graph.message import add_messages
from typing import TypedDict,Annotated
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import BaseMessage,SystemMessage,HumanMessage
from dotenv import load_dotenv
load_dotenv()

class ChatState(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

model=init_chat_model(
    "openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0.4
)

def chat_message(state:ChatState):
    response=model.invoke(state["messages"])
    return {"messages":[response]}

checkpoint=MemorySaver()
graph=StateGraph(ChatState)

graph.add_node("chat_message",chat_message)

graph.add_edge(START,"chat_message")
graph.add_edge("chat_message",END)

workflow=graph.compile(checkpointer=checkpoint)



