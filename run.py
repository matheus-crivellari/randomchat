from flask import Flask, Blueprint
from randomzap.home.views import home
from randomzap.chat.views import chat

app = Flask(__name__)
app.register_blueprint(home)
app.register_blueprint(chat)

if __name__ == '__main__':
	app.run(debug=True)

