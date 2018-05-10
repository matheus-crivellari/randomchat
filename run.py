from flask import Flask, Blueprint
from randomzap.home.views import home
from randomzap.chat.views import chat

from randomzap.chat.views import sio
import socketio
import eventlet
import eventlet.wsgi

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

if __name__ == '__main__':
	# app.run(debug=True)

	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('',8000)), app)