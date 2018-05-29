import os
import sys

from flask import Flask

from randomchat.home.views import home
from randomchat.chat.views import chat, sio

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

# sio.init_app(app)
# sio.run(app, debug=True)
app.run(host='0.0.0.0')