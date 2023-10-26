from flask import Flask

app = Flask(__name__)

from app.public import _public
app.register_blueprint(_public)

from app.api import _api
app.register_blueprint(_api, url_prefix="/api/")