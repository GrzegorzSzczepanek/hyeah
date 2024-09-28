import os
from typing import Annotated
from langchain_experimental.tools import PythonREPLTool
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from pydantic import BaseModel
from typing import Literal
import functools
import operator
from typing import Sequence
from typing_extensions import TypedDict
from langchain_core.messages import BaseMessage
from langgraph.graph import END, StateGraph, START
from langgraph.prebuilt import create_react_agent
from langchain.tools import BaseTool

openai_api_key = os.getenv("OPENAI_API_KEY")

class AnswerTool(BaseTool):
    name: str = "AnswerTool"
    description: str = "Use this tool to get a short answer to a question."

    def _run(self, query: str):
        local_llm = ChatOpenAI(model="gpt-4", temperature=0, max_tokens=50)
        response = local_llm.predict(query)
        return response

    async def _arun(self, query: str):
        raise NotImplementedError("Async not implemented")

answer_tool = AnswerTool()



def agent_node(state, agent, name):
    node_name = f"Agent Node: {name}"
    print(f"\n=== Executing Node: {node_name} ===")
    print(f"Input State: {state}")
    result = agent.invoke(state)
    output = {"messages": [HumanMessage(content=result["messages"][-1].content, name=name)]}
    print(f"Output State: {output}")
    print(f"\n======================")
    return output



# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str