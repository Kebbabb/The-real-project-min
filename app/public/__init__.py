from flask import Blueprint

_public = Blueprint('public', __name__, template_folder='templates')

from app.public import routes
