import threading
import time
from flask import Flask, request
from flask_socketio import SocketIO
from flask_cors import CORS
from xmlschema import XMLSchema
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

form_schema = XMLSchema("../Backend/form-schema.xsd")


class N:
    def __init__(self, data, children=[]):
        self.data = data
        self.children = children

    def print(self, level=0):
        indent = "  " * level
        print(f"{indent}{self.data}")
        for child in self.children:
            child.print(level + 1)


class PCC3:
    def __init__(self):
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
        print(self.form_pointer)
        return x

    def fill_data(self, data):
        self.form.children[self.form_pointer[0]].children[self.form_pointer[1]] = data

        if self.form_pointer[1] + 1 < len(
            self.form.children[self.form_pointer[0]].children
        ):
            self.form_pointer = (self.form_pointer[0], self.form_pointer[1] + 1)
        else:
            if self.form_pointer[0] + 1 < len(self.form.children):
                self.form_pointer = (self.form_pointer[0] + 1, 0)
            else:
                return None
        return data

    def validate(self):
        return form_schema.is_valid(self.to_xml())

    def serialize(self):
        return "TODO"


@app.route("/")
def index():
    return "hello, world"


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
                room=sid
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
        if last_activity and (time.time() - last_activity) >= 60:  # 5 seconds inactivity
            socketio.emit(
                "message",
                {"message": "Czy wciąz tu jesteś? W przypadku braku aktywność czat zostanie zamknięty."},
                room=sid
            )
            print(f"Sent inactivity warning to user {sid}")

            # Start a 15-second timer to close the session if no activity
            timer = threading.Timer(60, close_session, args=[sid])
            timer.start()
            user_timers[sid] = timer

@socketio.on("message")
def handle_message(msg):
    sid = request.sid
    current_time = time.time()
    
    print(f"Message from {sid}: {msg}")

    # Process the incoming message using your model
    for chunk in model.stream(str(msg)):
        print(chunk.content, end="", flush=True)
        obj = {"message": chunk.content}
        socketio.emit("message_chunk", obj, room=sid)

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