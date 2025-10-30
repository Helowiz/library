from datetime import datetime

from flask import flash, redirect, render_template, request, url_for, current_app, abort

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
    current_app.logger.info(f"Recherche du livre avec l'ID : {book_id}")
    
    try:
        book = Book.get_book_with_all_data(book_id)

        if book is None:
            current_app.logger.warning(f"Aucun livre trouvé pour l'ID : {book_id}. Renvoi d'une erreur 404.")
            abort(404) 

        current_app.logger.debug(f"Livre trouvé : {book}")
        return render_template("book/detail.html", book=book)

    except Exception as e:
        current_app.logger.error(
            f"Une erreur est survenue lors de la récupération du livre ID {book_id}", 
            exc_info=True
        )
        abort(500)


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
        
        Edition.get_or_create(
            isbn=isbn,
            published_date=published_date,
            cover_url=cover_url,
            pages=pages,
            language=language,
            book=new_book,
            publisher=publisher_instance,
        )

        kind_instance = Kind.get_or_create(name=request.form.get("genre").strip())
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
    book_id = request.form["book_id"]
    new_status = request.form["status"]    

    return redirect(url_for("book.detail_book", book_id=book_id))
