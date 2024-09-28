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
python_repl_tool = PythonREPLTool()
llm_model = "gpt-4o-mini"


class AnswerTool(BaseTool):
    name: str = "AnswerTool"
    description: str = "Use this tool to get a short answer to a question."

    def _run(self, query: str):
        local_llm = ChatOpenAI(model=llm_model, temperature=0, max_tokens=50)
        response = local_llm.predict(query)
        return response

    async def _arun(self, query: str):
        raise NotImplementedError("Async not implemented")


answer_tool = AnswerTool()

llm = ChatOpenAI(model=llm_model)


class routeResponse(BaseModel):
    next: Literal["FINISH", "Researcher", "Coder"]


def agent_node(state, agent, name):
    node_name = f"Agent Node: {name}"
    print(f"\n=== Executing Node: {node_name} ===")
    print(f"Input State: {state}")
    result = agent.invoke(state)
    output = {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }
    print(f"Output State: {output}")
    print(f"\n======================")
    return output


def supervisor_agent(state):
    supervisor_chain = prompt | llm.with_structured_output(routeResponse)
    result = supervisor_chain.invoke(state)
    print(f"\nSupervisor Decision: {result.next}")
    return {"next": result.next}


# The agent state is the input to each node in the graph
class AgentState(TypedDict):
    # The annotation tells the graph that new messages will always
    # be added to the current states
    messages: Annotated[Sequence[BaseMessage], operator.add]
    # The 'next' field indicates where to route to next
    next: str


members = ["Researcher", "Coder"]
system_prompt = (
    "You are a supervisor tasked with managing a conversation between the"
    " following workers:  {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
)
options = ["FINISH"] + members


prompt = ChatPromptTemplate.from_messages(
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


# Agents creation
research_agent = create_react_agent(llm, tools=[answer_tool])
research_node = functools.partial(agent_node, agent=research_agent, name="Researcher")


code_agent = create_react_agent(llm, tools=[python_repl_tool])
code_node = functools.partial(agent_node, agent=code_agent, name="Coder")

# Workflow creation
workflow = StateGraph(AgentState)
workflow.add_node("Researcher", research_node)
workflow.add_node("Coder", code_node)
workflow.add_node("supervisor", supervisor_agent)

for member in members:
    # We want our workers to ALWAYS "report back" to the supervisor when done
    workflow.add_edge(member, "supervisor")

conditional_map = {k: k for k in members}
conditional_map["FINISH"] = END
print(conditional_map)

workflow.add_conditional_edges("supervisor", lambda x: x["next"], conditional_map)

workflow.add_edge(START, "supervisor")


# Start the flow

graph = workflow.compile()

for s in graph.stream(
    {"messages": [HumanMessage(content="Give me a short recipe for a cake")]}
):
    if "__end__" not in s:
        print(s)
        print("----")
