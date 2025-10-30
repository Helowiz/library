from flask import render_template

from app.main import bp
from app.models.book import BookState


@bp.route("/")
def index():
    reading = BookState.get_reading_books()
    print(reading)
    return render_template("dashboard.html", books=reading)
