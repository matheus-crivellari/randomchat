from flask import Blueprint, render_template
from randomzap.settings import settings

import socketio
import random

# Configuration
# Event table
# Default built-in SocketIO events are not in the table
EVENTS = {
	'PAIRFOUND' : 'pairfound',
	'PAIRLOST'  : 'pairlost',
	'ALERT' 	: 'alert',
	'SKIP'  	: 'skip',
}

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
				pairs[i][0] = 'EMPTY'
				print('Pairs: ', pairs)
				return

			elif(pairs[i][1] == sid):
				pairs[i][1] = 'EMPTY'
				print('Pairs: ', pairs)
				return

			else:
				pass

			print('Not found')

# Add sid to a pair in pairs
def add_to_pair(sid,pairs,index):
	i = index
	if(pairs[i][0] is None):
		pairs[i][0] = sid
	elif(pairs[i][1] is None):
		pairs[i][1] = sid

	return pairs[i]

@chat.route('/chat')
def chat_index():
	return render_template('index.html', settings=settings)

@sio.on('connect', namespace='/chat')
def on_connect(sid, environ):
	print('Connected {}'.format(sid))

	tp = first_available_pair(pairs)
	if(tp): # If found an available pair
		pair = add_to_pair(sid, pairs, tp[1]) # Add new sid to pair

		if(pair): # If successfuly added to pair send PAIRFOUND event to both sids
			if(pair[0] is not None): 
				sio.emit(EVENTS['PAIRFOUND'], data={'msg':'You\'re now chatting with a random stranger. Say hello!'}, room=pair[0], namespace='/chat')

			if(pair[1] is not None):
				sio.emit(EVENTS['PAIRFOUND'], data={'msg':'You\'re now chatting with a random stranger. Say hello!'}, room=pair[1], namespace='/chat')

	else:
		pairs.append([sid, None])

	print('Pairs: ', pairs)


@sio.on('message', namespace='/chat')
def on_chat_message(sid, data):

	msg = data
	nsid = find_pair(sid,pairs)

	if(nsid):
		# Loggin the event to the console
		print('{} to {}: '.format(sid, nsid, msg))

		# Sending message to actual recipient (only if recipient is not None)
		sio.send(msg, room=nsid, namespace='/chat')

@sio.on(EVENTS['SKIP'], namespace='/chat')
def on_skip(sid):
	print('{} skipped conversation.'.format(sid))

	# Finds this sid pair
	psid = find_pair(sid, pairs)
	if(psid):
		# Notifies him/her about pair lost
		sio.emit(EVENTS['PAIRLOST'], data={'msg':'Stranger left the conversation.'}, room=psid, namespace='/chat')
	
	# Removes this sid from pair
	remove_from_pair(sid, pairs)

	# Shuffles pairs list before finding another pair to this sid
	random.shuffle(pairs)

	# Tries to find another pair
	tp = first_available_pair(pairs)

	# If found another pair
	if(tp):
		# Adds this sid to new pair
		pair = add_to_pair(sid, pairs, tp[1])

		# If successfuly added send notify both sids about new match
		if(pair): 
			if(pair[0] is not None): 
				sio.emit(EVENTS['PAIRFOUND'], data={'msg':'You\'re now chatting with a random stranger. Say hello!'}, room=pair[0], namespace='/chat')

			if(pair[1] is not None):
				sio.emit(EVENTS['PAIRFOUND'], data={'msg':'You\'re now chatting with a random stranger. Say hello!'}, room=pair[1], namespace='/chat')

	# If not found
	else:
		# Appends this sid to a new index in 
		# pairs list with an empty pair
		# in order to make this pairable again
		pairs.append([sid, None])


	# Must implement a check for ['EMPTY', 'EMPTY']
	# indexes in pairs list and clear them in order 
	# to free memory.
	# TO-DO
	# 
	# Must implement a trhead safe logic here
	# in order keep things ok.
	# TO-DO

	print('Pairs: ', pairs)


@sio.on('disconnect', namespace='/chat')
def on_disconnect(sid):
	psid = find_pair(sid, pairs)
	print('Notify {} that stranger left and remove stranger.'.format(psid))
	# Sending alert to actual recipient (only if recipient is not None)
	if(psid):
		sio.emit(EVENTS['PAIRLOST'], data={'msg':'Stranger left the conversation.'}, room=psid, namespace='/chat')
	
	remove_from_pair(sid, pairs)

