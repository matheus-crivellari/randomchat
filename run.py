import os
import sys

from flask import Flask, Blueprint
from randomchat.home.views import home
from randomchat.chat.views import chat

from randomchat.chat.views import sio
import socketio
import eventlet
import eventlet.wsgi

import logging

PORT = 5000

# This is an environment varaible created on Heroku app's running 
# O.S. via App Settings on Heroku dashboard.
# This is intended to make this app running both, locally and at Heroku's cloud.
if(os.environ.get('ON_HEROKU')):
	PORT = int(os.environ.get('PORT', 5000))

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

# Disable logs temporarily
# not meant for production
app.logger.setLevel(logging.NOTSET)

if __name__ == '__main__':
	# Checks if is there an cli argument 
	# called --socketio in argv list
	if('--socketio' in sys.argv):
		i = sys.argv.index('--socketio') # Finds its index
		i += 1
		if(sys.argv[i] == 'true'): # Checks if next argument list index is 'true'
			# If so, starts flask with socketio attached
			app = socketio.Middleware(sio, app)
			ioapp = eventlet.wsgi.server(eventlet.listen(('', PORT)), app)
		else:
			# If not, starts flask regular way
			app.run(debug=True)
			print('Tecoooo')
	else:
		# If no --socketio cli argument is passed, starts flask with socketio attached
		app = socketio.Middleware(sio, app)
		ioapp = eventlet.wsgi.server(eventlet.listen(('', PORT)), app)
