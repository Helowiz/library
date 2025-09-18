from flask import Blueprint

from app.book import routes as routes

bp = Blueprint("book", __name__)
