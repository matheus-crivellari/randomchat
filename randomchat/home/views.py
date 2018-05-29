from flask import Blueprint, render_template
from randomchat.settings import settings

home = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@home.route('/')
def index():
	return render_template('home/index.html', settings=settings)
