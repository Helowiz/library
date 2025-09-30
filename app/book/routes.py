from datetime import datetime

from flask import flash, redirect, render_template, request, url_for

from app.book import bp
from app.extensions import db
from app.models.author import Author
from app.models.book import Book, Kind
from app.models.publisher import Edition, Publisher


# READ
@bp.route("/")
def list_books():
    books = (
        db.session.query(Book.id, Book.title, Author.name, Edition.cover_url)
        .join(Author, Book.author_id == Author.id)
        .join(Edition, Book.id == Edition.book_id)
        .all()
    )
    return render_template("book/list.html", books=books)


@bp.route("/<int:book_id>")
def detail_book(book_id):
    book = (
        db.session.query(Book.title, Author.name, Edition.cover_url)
        .join(Author, Book.author_id == Author.id)
        .join(Edition, Book.id == Edition.book_id)
        .where(book_id == Book.id)
    )
    print(book)
    return render_template("book/detail.html", book=book)


# CREATE
@bp.route("/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form["title"]
        author = request.form["author"]
        synopsis = request.form.get("synopsis", "")
        publisher_name = request.form.get("publisher", "").strip()
        isbn = request.form.get("isbn")
        published_date = (
            datetime.strptime(request.form["published_date"], "%Y-%m-%d")
            if request.form.get("published_date")
            else None
        )
        cover_url = request.form["cover_url"]
        pages = int(request.form["pages"]) if request.form.get("pages") else None
        language = request.form["language"]

        author_instance = Author.get_or_create(author)
        new_book = Book.get_or_create(
            title=title, author_id=author_instance.id, synopsis=synopsis, status=None
        )
        publisher_instance = Publisher.get_or_create(publisher_name)
        new_edition = Edition.get_or_create(
            isbn=isbn,
            published_date=published_date,
            cover_url=cover_url,
            pages=pages,
            language=language,
            book=new_book,
            publisher=publisher_instance,
        )

        kind_instance = Kind(name=request.form.get("genre").strip())
        new_book.kinds.append(kind_instance)

        db.session.add(kind_instance)

        try:
            db.session.commit()
            flash("Book added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding book: {e}", "danger")
            return render_template("book/add.html", form_data=request.form)

        return redirect(url_for("book.list_books"))

    return render_template("book/add.html")


# UPDATE
@bp.route("/set-status", methods=["POST"])
def set_status():
    book_id = request.form.get("book_id")
    new_status = request.form.get("status")
    book = Book.query.get_or_404(book_id)

    if book.status == new_status:
        book.status = None
    else:
        book.status = new_status

    book.status = new_status
    db.session.commit()
    return redirect(url_for("book.detail_book", book_id=book_id))
