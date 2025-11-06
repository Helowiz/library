from flask import flash, redirect, render_template, url_for, abort

from app.book import bp
from app.extensions import db
from app.models.book import Book
from app.forms import BookForm, DeleteBookForm 


# READ
@bp.route("/")
def list_books():
    books = db.session.query(Book).all()
    return render_template("book/list.html", books=books)


@bp.route("/<int:book_id>")
def detail_book(book_id):
    delete_form = DeleteBookForm()
    book = Book.get_book_with_all_data(book_id)
    if not book:
        abort(404)
    return render_template("book/detail.html", book=book, delete_form=delete_form)

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

@bp.route('/book/edit/<int:book_id>/', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Livre mis à jour avec succès !')
        return redirect(url_for('book.detail_book', book_id=book.id))
        
    return render_template('book/edit.html', form=form, book=book)

@bp.route('/book/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    db.session.delete(book)
    db.session.commit()
    flash(f'Le livre "{book.title}" a été supprimé.', 'success')
    
    return redirect(url_for('main.index')) 
