from flask import Blueprint

from app.main import routes as routes

bp = Blueprint("main", __name__)
