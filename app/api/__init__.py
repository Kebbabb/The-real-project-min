from flask import Blueprint, Flask
from app import app

_api = Blueprint('api', __name__, template_folder='templates')
app.config["MONGO_URI"] = "mongodb+srv://MoonShadow:Sevilla123@moonshadow.vik8tcu.mongodb.net/globodain"
from . import routes