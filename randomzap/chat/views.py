from flask import Blueprint, render_template
from randomzap.settings import settings

chat = Blueprint('chat', __name__, template_folder='templates', static_folder='static')

@chat.route('/chat')
def chat_index():
	return render_template('index.html', settings=settings)