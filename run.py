from flask import Flask, Blueprint
from randomzap.home.views import home
from randomzap.chat.views import chat

from randomzap.chat.views import sio
import socketio
import eventlet
import eventlet.wsgi

import logging

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

# Disable logs temporarily
# not meant for production
app.logger.setLevel(logging.NOTSET)

if __name__ == '__main__':
	# app.run(debug=True)

	app = socketio.Middleware(sio, app)
	eventlet.wsgi.server(eventlet.listen(('',8000)), app)