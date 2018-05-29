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

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

# Disable logs temporarily
# not meant for production
app.logger.setLevel(logging.NOTSET)

sio.init_app(app)
sio.run(app)
exit()

print('Before initializing...')
if __name__ == '__main__' or os.environ.get('ON_HEROKU'):
	print('Initializing main app.')
	# Checks if is there an cli argument 
	# called --socketio in argv list
	if('--socketio' in sys.argv):
		i = sys.argv.index('--socketio') # Finds its index
		i += 1
		if(sys.argv[i] == 'true'): # Checks if next argument list index is 'true'
			# If so, starts flask with socketio attached
			print('Starting Flask app with SocketIO attached.')
			sio.init_app(app)
			sio.run(app, debug=True)
		else:
			# If not, starts flask regular way
			print('Starting regular Flask app.')
			app.run(debug=True)
	else:
		# If no --socketio cli argument is passed, starts flask with socketio attached
		print('Starting Flask app with SocketIO attached.')
		sio.init_app(app)
		sio.run(app, debug=True)
