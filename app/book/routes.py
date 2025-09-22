from flask import redirect, render_template, request, url_for

from app.book import bp
from app.extensions import db
from app.models import Book


# READ
@bp.route("/")
def list_books():
    books = Book.query.all()
    return render_template("book/list.html", books=books)


# CREATE
@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        new_book = Book(title=title, author=author)

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("book.list_books"))

    return render_template("book/add.html")
