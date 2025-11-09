from flask import render_template

from app.main import bp
from app.models.book import Book

@bp.route("/")
def index():
    book = Book.get_book_with_all_data(1)
    return render_template("dashboard.html", book=book)
