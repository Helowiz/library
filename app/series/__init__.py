from flask import Blueprint

bp = Blueprint("series", __name__)

from app.series import routes as routes
