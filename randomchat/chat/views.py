from flask import Blueprint, render_template
from randomchat.settings import settings

import socketio
import random
import logging

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

# Disable logs temporarily
# not meant for production
sio.logger.setLevel(logging.NOTSET)

pairs = []

# Returns a tuple containing the 
# firts non-full and non-empty pair 
# and its index.
# Returns None if no non-full 
# and non-empty pair found.
def first_available_pair(pairs):
	for i in range(0,len(pairs)):
		if(pairs[i] and isinstance(pairs[i], list)):
			pair = pairs[i]
			
			if (pair[0] is None and pair[1] is not None): # First is available and second is a user
				if(pair[1] == 'EMPTY'):
					pass
				else:
					return (pair, i)

			elif (pair[0] is not None and pair[1] is None): # First is a user and second is available
				if(pair[0] == 'EMPTY'):
					pass
				else:
					return (pair, i)

			else:
				pass

	return None

# Returns the respective pair sid for 
# given sid. Returns None if not found.
def find_pair(sid, pairs):
	for i in range(0,len(pairs)):
		if(pairs[i] and isinstance(pairs[i], list)):
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
		if(pairs[i] and isinstance(pairs[i], list)):
			if(pairs[i][0] == sid):
				pairs[i][0] = 'EMPTY'
				print('User removed.')
				print('Pairs: ', pairs)
				return

			elif(pairs[i][1] == sid):
				pairs[i][1] = 'EMPTY'
				print('User removed.')
				print('Pairs: ', pairs)
				return

			else:
				print('No user removed.')
				pass

# Add sid to a pair in pairs
def add_to_pair(sid, pairs, index):
	i = index
	if(pairs[i][0] is None):
		pairs[i][0] = sid
	elif(pairs[i][1] is None):
		pairs[i][1] = sid

	return pairs[i]

# Free space removing pairs with both spaces EMPTY
def free_space(pairs):

	pairs = [pair for pair in pairs if pair != ['EMPTY', 'EMPTY']]
	print('Memory space freed for more pairs to enter.')

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
			if(pair[0] is not None and pair[1] is not None): 
				sio.emit(EVENTS['PAIRFOUND'], data={'msg':'You\'re now chatting with a random stranger. Say hello!'}, room=pair[0], namespace='/chat')
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
		print('{} to {}: {}'.format(sid, nsid, msg))

		# Sending message to actual recipient (only if recipient is not None)
		sio.send(msg, room=nsid, namespace='/chat')

	free_space(pairs)
	print('Pairs: ', pairs)

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
	free_space(pairs)

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
		# pairs list with an None pair
		# in order to make this pairable again
		pairs.append([sid, None])


	free_space(pairs)

	print('Pairs: ', pairs)


@sio.on('disconnect', namespace='/chat')
def on_disconnect(sid):
	psid = find_pair(sid, pairs)
	print('Notify {} that stranger left and remove stranger.'.format(psid))
	# Sending alert to actual recipient (only if recipient is not None)
	remove_from_pair(sid, pairs)
	free_space(pairs)

	if(psid):
		sio.emit(EVENTS['PAIRLOST'], data={'msg':'Stranger left the conversation.'}, room=psid, namespace='/chat')