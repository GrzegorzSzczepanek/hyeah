from flask import Flask, jsonify
from flask_socketio import SocketIO, send
from flask_cors import CORS


app = Flask(__name__)
CORS(app, origins="http://localhost:3000")

socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000")


@app.route("/")
def index():
    return "hello, world"


@socketio.on("message")
def handle_message(msg):
    print(f"Message: {msg}")
    
    obj = {"sender": "bot", "message": f"Server received: {msg['message']}"}
    send(obj, broadcast=True)