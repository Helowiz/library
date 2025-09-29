from flask import render_template

from app.main import bp
from app.models import Book


@bp.route("/")
def index():
    books = Book.query.all()
    return render_template("dashboard.html", books=books)
