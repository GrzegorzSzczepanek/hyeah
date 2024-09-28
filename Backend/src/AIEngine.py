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
from AgentUtils import answer_tool, agent_node, AgentState

openai_api_key = os.getenv("OPENAI_API_KEY")

# System variables

members = ["Conversation", "Taxes"]
class routeResponse(BaseModel):
    next: Literal["FINISH", "Conversation", "Taxes"]
options = ["FINISH"] + members

system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
superVisorCheckPrompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Given the conversation above, who should act next?"
            " Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options), members=", ".join(members))

llm = ChatOpenAI(model="gpt-4")

# Supervisor 

def supervisor_agent(state):
    supervisor_chain = (
        superVisorCheckPrompt 
        | llm.with_structured_output(routeResponse)
    )
    result = supervisor_chain.invoke(state)
    print(f"\nSupervisor Decision: {result.next}")
    return {'next': result.next}


def defineGraph():
    #Agents creation
    conversationAgent = create_react_agent(llm, tools=[answer_tool])
    conversationNode = functools.partial(agent_node, agent=conversationAgent, name="Conversation")


    taxesAgent = create_react_agent(llm, tools=[answer_tool])
    taxesNode = functools.partial(agent_node, agent=taxesAgent, name="Taxes")

    #Workflow creation
    workflow = StateGraph(AgentState)
    workflow.add_node("Conversation", conversationNode)
    workflow.add_node("Taxes", taxesNode)
    workflow.add_node("Supervisor", supervisor_agent)

    for member in members:
        # We want our workers to ALWAYS "report back" to the supervisor when done
        workflow.add_edge(member, "Supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["FINISH"] = END
    print(conditional_map)

    workflow.add_conditional_edges("Supervisor", lambda x: x["next"], conditional_map)
    workflow.add_edge(START, "Supervisor")

    return workflow.compile()

def startEngine():
    graph = defineGraph()
    
    for s in graph.stream(
        {
            "messages": [
                HumanMessage(content="Give me a short recipe for a cake")
            ]
        }
    ):
        if "__end__" not in s:
            print(s)
            print("----")


if __name__ == "__main__":
    startEngine()


