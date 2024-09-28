from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from xmlschema import XMLSchema
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4o-mini")


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")

form_schema = XMLSchema("../Backend/form-schema.xsd")


def validate_form(form):
    return form_schema.is_valid(form)


@app.route("/")
def index():
    return "hello, world"


@socketio.on("message")
def handle_message(msg):
    print(f"Message: {msg}")
    
    for chunk in model.stream(str(msg)):
        print(chunk.content, end="", flush=True)
        
        obj = {"sender": "bot", "message": chunk.content}
        socketio.emit("message_chunk", obj) 

