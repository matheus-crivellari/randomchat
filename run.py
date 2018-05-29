import os
import sys

from flask import Flask

from randomchat.home.views import home
from randomchat.chat.views import chat, sio

app = Flask(__name__)
sio.init_app(app)

app.register_blueprint(home)
app.register_blueprint(chat)

if __name__ == "__main__":
	# app.run(debug=True)
	sio.run(app, debug=True)
