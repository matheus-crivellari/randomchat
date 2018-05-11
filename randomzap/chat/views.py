from flask import Blueprint, render_template
from randomzap.settings import settings

import socketio

chat = Blueprint('chat', __name__, template_folder='templates', static_folder='static')
sio  = socketio.Server()

pairs = []

# Returns a tuple containing the 
# firts non-full pair and its index
# or None if no non-full pair found
def first_available_pair(pairs):
	for i in range(0,len(pairs)):
		if(isinstance(pairs[i], list)):
			if(pairs[i][0] is None or pairs[i][1] is None):
				return (pairs[i], i)
			else:
				pass
	return None

# Returns the respective pair sid for 
# given sid. Returns None if not found.
def find_pair(sid, pairs):
	for i in range(0,len(pairs)):
		if(isinstance(pairs[i], list)):
			if(pairs[i][0] == sid):
				return pairs[i][1]
			elif(pairs[i][1] == sid):
				return pairs[i][0]
			else:
				None

# Clear the corresponding slot in a pair
# in order to make the pair available for 
# another user.
def remove_from_pair(sid, pairs):
	for i in range(0,len(pairs)):
		if(isinstance(pairs[i], list)):
			if(pairs[i][0] == sid):
				pairs[i][0] = None
				print('Pairs: ', pairs)
				return

			elif(pairs[i][1] == sid):
				pairs[i][1] = None
				print('Pairs: ', pairs)
				return

			else:
				pass

			print('Not found')

@chat.route('/chat')
def chat_index():
	return render_template('index.html', settings=settings)

@sio.on('connect', namespace='/chat')
def on_connect(sid, environ):
	print('Connected {}'.format(sid))

	tp = first_available_pair(pairs)
	if(tp):
		i = tp[1]
		if(pairs[i][0] is None):
			pairs[i][0] = sid
		else:
			pairs[i][1] = sid
	else:
		pairs.append([sid,None])

	print('Pairs: ', pairs)


@sio.on('message', namespace='/chat')
def on_chat_message(sid, data):

	msg = data
	nsid = find_pair(sid,pairs)
	# Loggin the event to the console
	print('{} to {}: '.format(sid, nsid, msg))

	# Sending message to actual recipient (only if recipient is not None)
	if(nsid):
		sio.send(msg, room=nsid, namespace='/chat')

@sio.on('skip', namespace='/chat')
def on_skip(sid):
	print('{} skipped conversation.'.format(sid))

@sio.on('disconnect', namespace='/chat')
def on_disconnect(sid):
	psid = find_pair(sid, pairs)
	print('Notify {} that stranger left and remove stranger.'.format(psid))
	# Sending alert to actual recipient (only if recipient is not None)
	if(psid):
		sio.emit('alert', data={'msg':'Stranger left the conversation.'}, room=psid, namespace='/chat')
	
	remove_from_pair(sid, pairs)

