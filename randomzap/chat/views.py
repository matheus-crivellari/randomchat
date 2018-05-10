from flask import Blueprint, render_template
from randomzap.settings import settings

import socketio

chat = Blueprint('chat', __name__, template_folder='templates', static_folder='static')
sio  = socketio.Server()

@chat.route('/chat')
def chat_index():
	return render_template('index.html', settings=settings)

@sio.on('connect', namespace='/chat')
def on_connect(sid, environ):
	print('Connected {}'.format(sid))

@sio.on('chat_message', namespace='/chat')
def on_chat_message(sid, data):
	msg = data['msg']
	print('Message', msg)

@sio.on('disconnect', namespace='/chat')
def on_disconnect(sid):
	print('Disconnected ', sid)
