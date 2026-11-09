import sys

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from app.llm import get_llm
from app.tools import TOOLS

SYSTEM_PROMPT = """You are the customer support agent for abhimart, an online store.
Use your tools to look up orders. Never guess order details.
Keep replies short and friendly."""

model = get_llm().bind_tools(TOOLS)


def call_model(state: MessagesState) -> dict:
    return {
        "messages": [model.invoke([SystemMessage(SYSTEM_PROMPT), *state["messages"]])]
    }


graph = (
    StateGraph(MessagesState)
    .add_node("agent", call_model)
    .add_node("tools", ToolNode(TOOLS))
    .add_edge(START, "agent")
    .add_conditional_edges("agent", tools_condition)
    .add_edge("tools", "agent")
    .compile()
)


if __name__ == "__main__":
    result = graph.invoke(
        {"messages": [HumanMessage(sys.argv[1])]}, {"recursion_limit": 5}
    )
    for message in result["messages"]:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                print(f"[tool] {call['name']}({call['args']})")
            if message.text:
                print(f"agent: {message.text}")
