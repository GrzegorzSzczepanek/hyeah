from flask import Flask
from flask_socketio import SocketIO, send

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return "hello, world"


@socketio.on("message")
def handle_message(msg):
    print(f"Message: {msg}")
    send(f"Server received: {msg}", broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000)
