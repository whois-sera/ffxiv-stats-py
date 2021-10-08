from flask import Blueprint

bp = Blueprint('hello', __name__, template_folder="templates")

from app.hello import routes