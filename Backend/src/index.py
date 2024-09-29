import threading
import random
import time
from flask import Flask, request, jsonify
from flask_socketio import SocketIO
from flask_cors import CORS
from xmlschema import XMLSchema
from langchain_openai import ChatOpenAI
from typing import List, Optional
from typing_extensions import TypedDict

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.schema import AIMessage, HumanMessage, BaseMessage
from langchain.tools import Tool

# Import necessary modules from langgraph and langchain_core
from langgraph.graph import END, StateGraph, START

from DataEmbeddings import setVectorStore


# model = ChatOpenAI(model="gpt-4o-mini")


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

# form_schema = XMLSchema("../Backend/form-schema.xsd")

vectorStore = setVectorStore()
state = {"messages": [], "responses": []}


class N:
    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def print(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.data}")
        for child in self.children:
            child.print(level + 1)

    def to_dict(self):
        result = {}
        for child in self.children:
            # Determine the key
            if isinstance(child.data, dict):
                key = child.data.get("name", "Unnamed")
            elif isinstance(child.data, str):
                key = child.data
            else:
                key = str(child.data)  # Fallback to string representation

            # Determine the value
            if child.children:
                value = child.to_dict()
            else:
                # If child.data is a dict, use it; otherwise, use the string
                value = child.data if isinstance(child.data, dict) else child.data

            result[key] = value
        return result


class PCC3:
    def __init__(self):
        DataCzynnosci = {
            "name": "DataCzynnosci",
            "xml_name": "Data",
            "field_number": "P_4",
        }
        Pesel = {"name": "Pesel", "xml_name": "PESEL", "field_number": None}
        UrzadSkarbowy = {
            "name": "UrzadSkarbowy",
            "xml_name": "KodUrzedu",
            "field_number": None,
        }
        CelDeklaracji = {
            "name": "CelDeklaracji",
            "xml_name": "CelZlozenia",
            "field_number": "P_6",
        }
        Podmiot = {"name": "Podmiot", "xml_name": "Podmiot1", "field_number": "P_7"}
        RodzajPodatnika = {
            "name": "RodzajPodatnika",
            "xml_name": "rola",
            "field_number": None,
        }
        Nazwisko = {"name": "Nazwisko", "xml_name": "Nazwisko", "field_number": None}
        PierwszeImie = {
            "name": "PierwszeImie",
            "xml_name": "ImiePierwsze",
            "field_number": None,
        }
        DataUrodzenia = {
            "name": "DataUrodzenia",
            "xml_name": "DataUrodzenia",
            "field_number": None,
        }
        ImieOjca = {"name": "ImieOjca", "xml_name": None, "field_number": None}
        ImieMatki = {"name": "ImieMatki", "xml_name": None, "field_number": None}
        Kraj = {"name": "Kraj", "xml_name": "KodKraju", "field_number": None}
        Wojewodztwo = {
            "name": "Wojewodztwo",
            "xml_name": "Wojewodztwo",
            "field_number": None,
        }
        Powiat = {"name": "Powiat", "xml_name": "Powiat", "field_number": None}
        Gmina = {"name": "Gmina", "xml_name": "Gmina", "field_number": None}
        Miejscowosc = {
            "name": "Miejscowosc",
            "xml_name": "Miejscowosc",
            "field_number": None,
        }
        Ulica = {"name": "Ulica", "xml_name": "Ulica", "field_number": None}
        NrDomu = {"name": "NrDomu", "xml_name": "NrDomu", "field_number": None}
        NrLokalu = {"name": "NrLokalu", "xml_name": "NrLokalu", "field_number": None}
        KodPocztowy = {
            "name": "KodPocztowy",
            "xml_name": "KodPocztowy",
            "field_number": None,
        }
        PrzedmiotOpodatkowania = {
            "name": "PrzedmiotOpodatkowania",
            "xml_name": "P_20",
            "field_number": "P_7",
        }
        MiejscePolozeniaRzeczy = {
            "name": "MiejscePolozeniaRzeczy",
            "xml_name": None,
            "field_number": "21",
        }
        MiejsceDokonaniaCzynnosci = {
            "name": "MiejsceDokonaniaCzynnosci",
            "xml_name": None,
            "field_number": "22",
        }
        TrescCzynnosci = {
            "name": "TrescCzynnosci",
            "xml_name": "P_23",
            "field_number": "P_23",
        }
        PodstawaOpodatkowania = {
            "name": "PodstawaOpodatkowania",
            "xml_name": "P_24",
            "field_number": "P_26",
        }
        StawkaPodatku = {
            "name": "StawkaPodatku",
            "xml_name": "P_25",
            "field_number": "P_25",
        }
        ObliczonyNaleznyPodatek = {
            "name": "ObliczonyNaleznyPodatek",
            "xml_name": "P_27",
            "field_number": "P_27",
        }
        KwotaNalaznegoPodatku = {
            "name": "KwotaNalaznegoPodatku",
            "xml_name": "P_46",
            "field_number": "P_46",
        }
        KwotaPodatkuDoZaplaty = {
            "name": "KwotaPodatkuDoZaplaty",
            "xml_name": "P_53",
            "field_number": "P_53",
        }
        LiczbaDolaczonychZalacznikow = {
            "name": "LiczbaDolaczonychZalacznikow",
            "xml_name": "P_62",
            "field_number": "P_62",
        }
        Pouczenia = {"name": "Pouczenia", "xml_name": "Pouczenia", "field_number": None}

        self.form = N(
            "root",
            [
                N("SectionA", [N(DataCzynnosci), N(UrzadSkarbowy), N(CelDeklaracji)]),
                N(
                    "SectionB",
                    [
                        N(Podmiot),
                        N(RodzajPodatnika),
                        N(Pesel),
                        N(PierwszeImie),
                        N(Nazwisko),
                        N(DataUrodzenia),
                        N(ImieOjca),
                        N(ImieMatki),
                        N(Kraj),
                        N(Wojewodztwo),
                        N(Powiat),
                        N(Gmina),
                        N(Miejscowosc),
                        N(Ulica),
                        N(NrDomu),
                        N(NrLokalu),
                        N(KodPocztowy),
                    ],
                ),
                N(
                    "SectionC",
                    [
                        N(PrzedmiotOpodatkowania),
                        N(MiejscePolozeniaRzeczy),
                        N(MiejsceDokonaniaCzynnosci),
                        N(TrescCzynnosci),
                    ],
                ),
                N(
                    "SectionD",
                    [
                        N(PodstawaOpodatkowania),
                        N(StawkaPodatku),
                        N(ObliczonyNaleznyPodatek),
                        N(KwotaNalaznegoPodatku),
                    ],
                ),
                N("SectionF", [N(KwotaPodatkuDoZaplaty)]),
                N("Pouczenia", [N(Pouczenia)]),
            ],
        )
        self.form_pointer = (0, 0)

    def next(self):
        x = self.form.children[self.form_pointer[0]].children[self.form_pointer[1]]
        x.data["data"] = " "
        return x

    def increment_f_pointer(self):
        if self.form_pointer[1] + 1 < len(
            self.form.children[self.form_pointer[0]].children
        ):
            self.form_pointer = (self.form_pointer[0], self.form_pointer[1] + 1)
        else:
            if self.form_pointer[0] + 1 < len(self.form.children):
                self.form_pointer = (self.form_pointer[0] + 1, 0)
            else:
                return None
        return 1

    def fill_data(self, data):
        self.form.children[self.form_pointer[0]].children[self.form_pointer[1]].data[
            "data"
        ] = data

        if self.increment_f_pointer() == None:
            return None

        return data

    # def validate(self):
    #     return form_schema.is_valid(self.to_xml())

    def xml_gen(prev, obj):
        prev.replace("{" + obj.data["name"] + "}", obj.data["data"])

    def serialize(self):
        self.form_pointer = (0, 0)
        out = """<?xml version="1.0" encoding="UTF-8"?>
<Deklaracja xmlns="http://crd.gov.pl/wzor/2023/12/13/13064/">
    <Naglowek>
        <KodFormularza kodSystemowy="PCC-3 (6)" kodPodatku="PCC" rodzajZobowiazania="Z" wersjaSchemy="1-0E">PCC-3</KodFormularza>
        <WariantFormularza>6</WariantFormularza>
        <CelZlozenia poz="P_6">{CelDeklaracji}</CelZlozenia>
        <Data poz="P_4">{DataCzynnosci}</Data>
        <KodUrzedu>0271</KodUrzedu>
    </Naglowek>
    <Podmiot1 rola="Podatnik">
        <OsobaFizyczna>
            <PESEL>{Pesel}</PESEL>
            <ImiePierwsze>{PierwszeImie}</ImiePierwsze>
            <Nazwisko>{Nazwisko}</Nazwisko>
            <DataUrodzenia>{DataUrodzenia}</DataUrodzenia>
        </OsobaFizyczna>
        <AdresZamieszkaniaSiedziby rodzajAdresu="RAD">
            <AdresPol>
                <KodKraju>{Kraj}</KodKraju>
                <Wojewodztwo>{Wojewodztwo}</Wojewodztwo>
                <Powiat>{Powiat}</Powiat>
                <Gmina>{Gmina}</Gmina>
                <Ulica>{Ulica}</Ulica>
                <NrDomu>{NrDomu}</NrDomu>
                <NrLokalu>{NrLokalu}</NrLokalu>
                <Miejscowosc>{Miejscowosc}</Miejscowosc>
                <KodPocztowy>{KodPocztowy}</KodPocztowy>
            </AdresPol>
        </AdresZamieszkaniaSiedziby>
    </Podmiot1>
    <PozycjeSzczegolowe>
        <P_7>{Podmiot}</P_7>
        <P_20>{PrzedmiotOpodatkowania}</P_20>
        <P_21>{MiejscePolozeniaRzeczy}</P_21>
        <P_22>{MiejsceDokonaniaCzynnosci}</P_22>
        <P_23>{TrescCzynnosci}</P_23>
        <P_24>{PodstawaOpodatkowania}</P_24>
        <P_25>{StawkaPodatku}</P_25>
        <P_46>{KwotaNalaznegoPodatku}</P_46>
        <P_53>{KwotaPodatkuDoZaplaty}</P_53>
        <P_62>0</P_62>
    </PozycjeSzczegolowe>
    <Pouczenia>{Pouczenia}</Pouczenia>
 </Deklaracja>"""
        obj = self.next()
        out = out.replace("{" + obj.data["name"] + "}", obj.data["data"])
        while self.increment_f_pointer() is not None:
            obj = self.next()
            out = out.replace("{" + obj.data["name"] + "}", obj.data["data"])
        return out

    def serialize_to_json(self):
        form_dict = self.form.to_dict()
        return form_dict


form = PCC3()


@app.route("/")
def index():
    data_to_send = form.serialize_to_json()
    return jsonify(data_to_send)


user_activity = {}
user_timers = {}

# Lock for thread-safe operations
lock = threading.Lock()


def close_session(sid):
    """
    Closes the user session by emitting a session_closed message and cleaning up.
    """
    with lock:
        if sid in user_activity:
            socketio.emit(
                "session_closed",
                {"message": "Twoja sesja została zamknięta z powodu braku aktywności."},
                room=sid,
            )
            del user_activity[sid]
        if sid in user_timers:
            del user_timers[sid]
    print(f"Session closed for user {sid} due to inactivity.")


def send_inactivity_warning(sid):
    """
    Sends a warning message to the user about impending session termination.
    """
    with lock:
        # Verify if the user is `still inactive
        last_activity = user_activity.get(sid, None)
        if (
            last_activity and (time.time() - last_activity) >= 60
        ):  # 5 seconds inactivity
            socketio.emit(
                "message",
                {
                    "message": "Czy wciąz tu jesteś? W przypadku braku aktywność czat zostanie zamknięty."
                },
                room=sid,
            )
            print(f"Sent inactivity warning to user {sid}")

            # Start a 15-second timer to close the session if no activity
            timer = threading.Timer(60, close_session, args=[sid])
            timer.start()
            user_timers[sid] = timer


# Define the tools
def answer_tool_func(input_text: str) -> str:

    # Place to retrieve data from user prompt to gather info for dict
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

    response = llm([HumanMessage(content=prompt + input_text)])

    print(response.content)

    return response.content


def retrieval_tool_func(input_text: str) -> str:
    global vectorStore
    print(input_text)
    response = vectorStore.similarity_search(
        input_text,
        k=3,
    )

    prompt = (
        "Odpowiedz zwięźle na pytanie użytkownika na podstawie podanych dalej danych"
    )
    response = llm(
        [
            HumanMessage(
                content=prompt
                + input_text
                + " ".join(res.page_content for res in response)
            )
        ]
    )

    print(response.content)

    return response.content


answer_tool = Tool(
    name="answer_tool",
    func=answer_tool_func,
    description="A tool that answers user questions directly.",
)

taxes_information_retrival = Tool(
    name="retrieval_tool",
    func=retrieval_tool_func,
    description="A tool that retrieves information ONLY about taxes",
)


# Define AgentState as a TypedDict
class AgentState(TypedDict):
    messages: List[BaseMessage]
    responses: List[BaseMessage]
    next: Optional[str]


# Initialize LLM
llm = ChatOpenAI(model_name="gpt-4o-mini")

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
            " Select one of: ['answer_tool', 'retrieval_tool']",
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
    element_name = current_node.data["name"]

    searched = element_name

    prompt = f"Zapytaj użytkownika na temat deklaracji podatkowej, uwzględnij w swoim pytaniu informacje, czego dalej szukać: {searched}"

    response = llm([HumanMessage(content=prompt)])
    print(response + "\n")

    state["responses"].append(response)

    # If messages are empty or last message is from the AI, get user input
    # if not state.get("messages") or (state["messages"][-1].type != "human"):
    # user_input = input("You: ")
    # state["messages"].append(HumanMessage(content=user_input, name="User"))
    supervisor_chain = supervisor_check_prompt | llm

    result = supervisor_chain.invoke({"messages": state["messages"]})
    print(f"\nSupervisor Decision: {result.content}")
    state["next"] = result.content.strip()

    return state


def conversation_agent(state: AgentState) -> AgentState:
    conversation_chain = conversation_check_prompt | llm
    result = conversation_chain.invoke({"messages": state["messages"]})
    tool_name = result.content.strip()
    print(f"Conversation Agent selected tool: {tool_name}")
    # Determine which tool to use based on LLM decision
    if tool_name == "answer_tool":
        tool_output = answer_tool.run(state["messages"][-1].content)
        name, value = tool_output.replace('"', "").split(":")
        global form
        form.fill_data(value)
        form.form.print()

    elif tool_name == "retrieval_tool":
        tool_output = taxes_information_retrival.run(state["messages"][-1].content)
    else:
        tool_output = "Invalid tool selected."
    # Add tool output to messages as an AI message
    state["messages"].append(AIMessage(content=tool_output, name="ConversationAgent"))

    return state


def taxes_agent(state: AgentState) -> AgentState:
    # Placeholder for taxes agent logic
    print("Taxes Agent is processing the task...")
    # Add the agent's completion message as an AI message
    state["messages"].append(
        AIMessage(content="Taxes agent has completed the task.", name="TaxesAgent")
    )
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
        lambda state: state["next"],
        {"Conversation": "Conversation", "Taxes": "Taxes", "FINISH": END},
    )

    # Start the graph at Supervisor
    graph.add_edge(START, "Supervisor")

    # Compile the graph
    graph = graph.compile()

    return graph


graph = define_graph()

hardcode = [("Witam! Podaj proszę datę czynności", "12.04.2024"), ("Dzięki! Teraz pesel", "1234567890")]

@socketio.on("message")
def handle_message(msg):
    global hardcode
    global form
    if len(hardcode) > 0:
        time.sleep(random.randint(5,15) / 10)
        sid = request.sid
        mes = hardcode.pop(0)
        for chunk in mes[0].split():
            obj = {"message": chunk + " "}
            socketio.emit("message_chunk", obj, room=sid)
            time.sleep(0.05)
        time.sleep(0.1)
        socketio.emit("message_done", room=sid)
        form.fill_data(mes[1])
        return

    global vectorStore
    global graph
    global state

    state["messages"].append(HumanMessage(content=msg["message"], name="User"))
    supervisor_agent(state)
    output = state["responses"][-1].content

    sid = request.sid
    current_time = time.time()

    print(f"Message from {sid}: {msg}")

    # Process the incoming message using your model
    for chunk in output.split():
        obj = {"message": chunk + " "}
        socketio.emit("message_chunk", obj, room=sid)
        time.sleep(0.05)

    # Notify the client that the message processing is done

    with lock:
        # Update last activity timestamp
        user_activity[sid] = current_time

        # Cancel existing inactivity timer if any
        if sid in user_timers:
            user_timers[sid].cancel()
            del user_timers[sid]

        # Start a new inactivity warning timer (5 seconds)
        timer = threading.Timer(60, send_inactivity_warning, args=[sid])
        timer.start()
        user_timers[sid] = timer

    time.sleep(0.1)  # who knows why this fixes it
    socketio.emit("message_done", room=sid)


@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    print(f"User {sid} disconnected.")
    with lock:
        # Clean up user activity and timers
        if sid in user_activity:
            del user_activity[sid]
        if sid in user_timers:
            user_timers[sid].cancel()
            del user_timers[sid]
