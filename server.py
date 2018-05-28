from flask import Flask, render_template
from flask_socketio import SocketIO
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route("/")
def index():
    return render_template('index.html')

@socketio.on('send_message')
def handle_source(json_data):
    echo = json_data['message']
    echo = 'Server Says: {}'.format(echo)
    print('Teco ', echo)
    socketio.emit('echo', {'echo': echo})

if __name__ == "__main__":
    socketio.run(app, debug=True)
