from datetime import datetime

from flask import flash, redirect, render_template, request, url_for, current_app, abort

from app.book import bp
from app.extensions import db
from app.models.book import Book


# READ
@bp.route("/")
def list_books():
    books = db.session.query(Book).all()
    return render_template("book/list.html", books=books)


@bp.route("/<int:book_id>")
def detail_book(book_id):
    book = Book.get_book_with_all_data(book_id)
    if not book:
        abort(404)
    return render_template("book/detail.html", book=book)

# CREATE
@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title")
        author = request.form.get("author")
        synopsis = request.form.get("synopsis", "")
        url = request.form.get("url", "")

        if not title or not author:
            flash("Title and Author are required fields.", "danger")
            return redirect(url_for("book.add_book"))

        book = Book.get_or_create(title=title, author=author, synopsis=synopsis, url=url)
        if book:
            flash(f"Book '{title}' added successfully.", "success")
            return redirect(url_for("book.detail_book", book_id=book.id))

    return render_template("book/add.html")


