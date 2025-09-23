from flask import render_template

from app.main import bp
from app.models import Book


@bp.route("/")
def index():
    books = Book.query.all()
    readings = [book for book in books if book.status == "reading"]
    reading = readings[0] if readings[0] else None
    return render_template("dashboard.html", books=books, reading=reading)
