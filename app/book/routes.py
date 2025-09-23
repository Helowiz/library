from datetime import datetime

from flask import redirect, render_template, request, url_for

from app.book import bp
from app.extensions import db
from app.models import Book


# READ
@bp.route("/")
def list_books():
    books = Book.query.all()
    return render_template("book/list.html", books=books)


@bp.route("/<int:book_id>")
def detail_book(book_id):
    book = Book.query.get_or_404(book_id)
    return render_template("book/detail.html", book=book)


# CREATE
@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        cover_url = request.form.get("cover_url")
        synopsis = request.form.get("synopsis")
        genre = request.form.get("genre")
        language = request.form.get("language")
        isbn = request.form.get("isbn")
        publisher = request.form.get("publisher")
        review = request.form.get("review")
        pages = int(request.form["pages"]) if request.form.get("pages") else None
        rating = float(request.form["rating"]) if request.form.get("rating") else None
        published_date = (
            datetime.strptime(request.form["published_date"], "%Y-%m-%d")
            if request.form.get("published_date")
            else None
        )
        is_read = "is_read" in request.form
        is_favorite = "is_favorite" in request.form

        new_book = Book(
            title=title,
            author=author,
            cover_url=cover_url,
            synopsis=synopsis,
            genre=genre,
            language=language,
            isbn=isbn,
            publisher=publisher,
            review=review,
            pages=pages,
            rating=rating,
            published_date=published_date,
            is_read=is_read,
            is_favorite=is_favorite,
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect(url_for("book.list_books"))

    return render_template("book/add.html")
