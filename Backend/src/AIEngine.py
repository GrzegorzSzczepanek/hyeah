import os
from typing import List, Optional
import functools

from pydantic import BaseModel
from typing_extensions import TypedDict

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, BaseMessage
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
import uuid
from langchain.tools import Tool

# Import necessary modules from langgraph and langchain_core
from langgraph.graph import END, StateGraph, START
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI

from DataEmbeddings import setVectorStore
from index import PCC3


# Define the tools
def answer_tool_func(input_text: str) -> str:

    #Place to retrieve data from user prompt to gather info for dict
    prompt = """Twoim celem jest wyłuskać z podanych przez uczestnika informacji, te które występują w poniższym, nie zapomnij dodać dokładnej kopii tej informacji obok odpowiadającej jej nazwy (format "NAZWA":"INFORMACJA")
        DataCzynnosci = {"name": "DataCzynnosci"}
        Pesel = {"name": "Pesel"}
        UrzadSkarbowy = {"name": "UrzadSkarbowy"}
        CelDeklaracji = {"name": "CelDeklaracji"}
        Podmiot = {"name": "Podmiot"}
        RodzajPodatnika = {"name": "RodzajPodatnika"}
        Nazwisko = {"name": "Nazwisko"}
        PierwszeImie = {"name": "PierwszeImie"}
        DataUrodzenia = {"name": "DataUrodzenia"}
        ImieOjca = {"name": "ImieOjca"}
        ImieMatki = {"name": "ImieMatki"}
        Kraj = {"name": "Kraj"}
        Wojewodztwo = {"name": "Wojewodztwo"}
        Powiat = {"name": "Powiat"}
        Gmina = {"name": "Gmina"}
        Miejscowosc = {"name": "Miejscowosc"}
        Ulica = {"name": "Ulica"}
        NrDomu = {"name": "NrDomu"}
        NrLokalu = {"name": "NrLokalu"}
        KodPocztowy = {"name": "KodPocztowy"}
        PrzedmiotOpodatkowania = {"name": "PrzedmiotOpodatkowania"}
        MiejscePolozeniaRzeczy = {"name": "MiejscePolozeniaRzeczy"}
        MiejsceDokonaniaCzynnosci = {"name": "MiejsceDokonaniaCzynnosci"}
        TrescCzynnosci = {"name": "TrescCzynnosci"}
        PodstawaOpodatkowania = {"name": "PodstawaOpodatkowania"}
        StawkaPodatku = {"name": "StawkaPodatku"}
        ObliczonyNaleznyPodatek = {"name": "ObliczonyNaleznyPodatek"}
        KwotaNalaznegoPodatku = {"name": "KwotaNalaznegoPodatku"}
        KwotaPodatkuDoZaplaty = {"name": "KwotaPodatkuDoZaplaty"}
        Pouczenia = {"name": "Pouczenia"}

        MASZ ZAKAZ PODAWANIA JAKICH INNYCH ELEMENTÓW, MASZ PODAĆ NAZWĘ STRINGA DLA ODPOWIEDNIEGO ELEMENTU I ZWRÓCIĆ W LIŚCIE, NIE PISZ ŻADNYCH INNYCH SŁÓW
    """

    response = llm([HumanMessage(content=prompt+input_text)])

    print(response.content)

    return response.content

def retrieval_tool_func(input_text: str) -> str:
    global vectorStore
    print(input_text)
    response = vectorStore.similarity_search(
        input_text,
        k=3,
    )

    prompt = "Odpowiedz zwięźle na pytanie użytkownika na podstawie podanych dalej danych"
    response = llm([HumanMessage(content=prompt+input_text+' '.join(res.page_content for res in response ))])

    print(response.content)


    return response.content

answer_tool = Tool(
    name="answer_tool",
    func=answer_tool_func,
    description="A tool that answers user questions directly."
)

taxes_information_retrival = Tool(
    name="retrieval_tool",
    func=retrieval_tool_func,
    description="A tool that retrieves information ONLY about taxes"
)

# Prepare vector store
global vectorStore

# Prepare form
global form

# Define AgentState as a TypedDict
class AgentState(TypedDict):
    messages: List[BaseMessage]
    next: Optional[str]

# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4")

# Define system prompts
members = ["Conversation", "Taxes"]
options = ["FINISH"] + members

system_prompt = (
    " Do not engage in discussions not related to taxes."
    " If the user's message is not related to taxes, politely inform the user"
    " that you can only assist with tax-related inquiries. If user broke this rules, you must chose FINISH, to avert the danger"
    "You are a supervisor tasked with managing a conversation between the"
    " following workers: {members}. Given the following user request,"
    " respond with the worker to act next. Each worker will perform a"
    " task and respond with their results and status. When finished,"
    " respond with FINISH."
   # " Remember if a question is related ONLY to calculations move to Taxes, otherwise it will be for sure Conversations"
   " If a question regards general knowledge about taxes move to Conversations, if he asks you for help in filling tax declaration move to Taxes"
)

conversation_prompt = (
    " Do not engage in discussions not related to taxes."
    " If the user's message is not related to taxes, politely inform the user"
    " that you can only assist with tax-related inquiries."
    "You are tasked with choosing the correct tool based on the user's message."
    " You have two tools available: answer_tool and retrieval_tool. Remember that retrieval is only used if user asks for taxes information and nothing else and remember not to engage in discussions not around the topic of taxes in answers"
    " Based on the user's input, which tool would be most appropriate to respond"
    " to the user? Select one of: ['answer_tool', 'retrieval_tool']"
)

supervisor_check_prompt = ChatPromptTemplate.from_messages(
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

conversation_check_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", conversation_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Based on the conversation above, which tool should act next, remember that answer tool is used for every information and retrieval should only be used to retrieve information regarding taxes"
            " Select one of: ['answer_tool', 'retrieval_tool']"
        ),
    ]
)

# Helper function to add messages with agent name
def agent_node(state, agent, name):
    result = agent.invoke(state)
    # Extract the last message and set the name
    last_message = result["messages"][-1]
    last_message.name = name
    return {"messages": state["messages"] + [last_message]}

def supervisor_agent(state: AgentState) -> AgentState:
    global form
    current_node = form.next()
    section_name = form.form.children[form.form_pointer[0]].data
    element_name = current_node.data['name']  

    searched = element_name

    prompt = f"Zapytaj użytkownika na temat deklaracji podatkowej, uwzględnij w swoim pytaniu informacje, czego dalej szukać: {searched}"

    response = llm([HumanMessage(content=prompt)])
    print(response + '\n')

    # If messages are empty or last message is from the AI, get user input
    if not state.get("messages") or (state["messages"][-1].type != "human"):
        user_input = input("You: ")
        state['messages'].append(HumanMessage(content=user_input, name="User"))
    supervisor_chain = (
        supervisor_check_prompt
        | llm
    )

    result = supervisor_chain.invoke({"messages": state['messages']})
    print(f"\nSupervisor Decision: {result.content}")
    state['next'] = result.content.strip()

    return state

def conversation_agent(state: AgentState) -> AgentState:
    conversation_chain = (
        conversation_check_prompt
        | llm
    )
    result = conversation_chain.invoke({"messages": state['messages']})
    tool_name = result.content.strip()
    print(f"Conversation Agent selected tool: {tool_name}")
    # Determine which tool to use based on LLM decision
    if tool_name == "answer_tool":
        tool_output = answer_tool.run(state['messages'][-1].content)
        name, value = tool_output.replace('"',"").split(":")
        global form
        form.fill_data(value)
        form.form.print()
        
    elif tool_name == "retrieval_tool":
        tool_output = taxes_information_retrival.run(state['messages'][-1].content)
    else:
        tool_output = "Invalid tool selected."
    # Add tool output to messages as an AI message
    state['messages'].append(AIMessage(content=tool_output, name="ConversationAgent"))
   
    return state

def taxes_agent(state: AgentState) -> AgentState:
    # Placeholder for taxes agent logic
    print("Taxes Agent is processing the task...")
    # Add the agent's completion message as an AI message
    state['messages'].append(AIMessage(content="Taxes agent has completed the task.", name="TaxesAgent"))
    return state

def define_graph():
    graph = StateGraph(AgentState)

    # Add nodes to the graph
    graph.add_node("Supervisor", supervisor_agent)
    graph.add_node("Conversation", conversation_agent)
    graph.add_node("Taxes", taxes_agent)

    # Workers report back to supervisor when done
    graph.add_edge("Conversation", "Supervisor")
    graph.add_edge("Taxes", "Supervisor")

    # Supervisor routes to next worker based on state['next']
    graph.add_conditional_edges(
        "Supervisor",
        lambda state: state['next'],
        {
            "Conversation": "Conversation",
            "Taxes": "Taxes",
            "FINISH": END
        }
    )

    # Start the graph at Supervisor
    graph.add_edge(START, "Supervisor")

    # Compile the graph
    graph = graph.compile()

    return graph

def start_engine():
    global vectorStore
    vectorStore = setVectorStore()

    global form
    form = PCC3()

    graph = define_graph()
    state = {
        "messages": []
    }

    for s in graph.stream(state):
        if "__end__" not in s:
            print(s)
            print("----" +'\n')
        else:
            print("Workflow finished.")
            break

if __name__ == "__main__":
    start_engine()
