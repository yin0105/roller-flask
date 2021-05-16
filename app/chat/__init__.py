from flask import Blueprint

chat_blueprint = Blueprint('chat', __name__, template_folder='templates')

from app.chat import routes, models, sockets