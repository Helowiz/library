from flask import flash, redirect, render_template, url_for, abort

from app.book import bp
from app.extensions import db
from app.models.book import Book
from app.forms import BookForm


# READ
@bp.route("/")
def list_books():
    return render_template("book/list.html")


@bp.route("/<int:book_id>")
def detail_book(book_id):
    book = Book.get_book_with_all_data(book_id)
    if not book:
        abort(404)
    return render_template("book/detail.html", book=book)

# CREATE

@bp.route("/add", methods=["GET", "POST"])
def add_book():
    form = BookForm()
    
    if form.validate_on_submit():
        new_book = Book(
            title=form.title.data,
            author=form.author.data,
            synopsis=form.synopsis.data,
            url=form.url.data
        )
        
        db.session.add(new_book)
        db.session.commit()
        
        flash(f"Le livre '{new_book.title}' a été ajouté avec succès !", "success")
        return redirect(url_for('book.detail_book', book_id=new_book.id))
    return render_template('book/add.html', form=form)


