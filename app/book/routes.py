from flask import render_template, request, url_for, redirect
from app.book import bp
from app.extensions import db
from app.models.book import Book


@bp.route("/")
def index():
    books = Book.query.all()
    return render_template("book/index.html", books=books)


@bp.route("/add/", methods=("GET", "POST"))
def add():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]

        book = Book(title=title, author=author)

        db.session.add(book)
        db.session.commit()

        return redirect(url_for("book.index"))

    return render_template("book/add.html")


@bp.route("/delete/")
def delete():
    return render_template("book/delete.html")


@bp.route("/update/")
def update():
    return render_template("book/update.html")
