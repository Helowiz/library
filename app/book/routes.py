from flask import flash, redirect, render_template, url_for, abort, request

from app.book import bp
from app.extensions import db
from app.models.book import Book
from app.forms import BookForm, DeleteBookForm 
from app.models.reading import BookStatus, Reading



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
    return render_template("book/detail.html", book=book, delete_form=delete_form, BookStatus=BookStatus)

# CREATE

@bp.route("/add", methods=["GET", "POST"])
def add_book():
    form = BookForm()
    
    if form.validate_on_submit():
        new_book = Book.get_or_create(
            title=form.title.data,
            author=form.author.data,
            synopsis=form.synopsis.data,
            url=form.url.data,
            number_of_pages=form.number_of_pages.data
        )

        return redirect(url_for('book.detail_book', book_id=new_book.id))
    return render_template('book/add.html', form=form)

# UPDATE

@bp.route('/edit/<int:book_id>/', methods=['GET', 'POST'])
def edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    form = BookForm(obj=book)
    
    if form.validate_on_submit():
        form.populate_obj(book)
        db.session.commit()
        flash('Livre mis à jour avec succès !')
        return redirect(url_for('book.detail_book', book_id=book.id))
        
    return render_template('book/edit.html', form=form, book=book)

@bp.route('/book/<int:book_id>/status', methods=['POST'])
def update_status(book_id):
    book = Book.query.get_or_404(book_id)
    status_key = request.form.get('status')

    if status_key in BookStatus.__members__:
        
        new_status = BookStatus[status_key]
        
        if not book.reading_status:
            book.reading_status = Reading()

        book.reading_status.status = new_status
        db.session.commit()
        
        flash(f'Le statut du livre a été mis à jour : "{new_status.value}"', 'success')
    else:
        flash('Statut non valide.', 'danger')

    return redirect(url_for('book.detail_book', book_id=book.id))

@bp.route('/book/<int:book_id>/progress', methods=['POST'])
def update_progress(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        pages_read = int(request.form.get('pages_read', 0))
    except ValueError:
        flash('Veuillez entrer un nombre valide de pages lues.', 'danger')
        return redirect(url_for('book.detail_book', book_id=book.id))

    if pages_read < 0 or pages_read > book.number_of_pages:
        flash('Le nombre de pages lues doit être entre 0 et le nombre total de pages du livre.', 'danger')
    else:
        if not book.reading_status:
            book.reading_status = Reading()

        book.reading_status.current_page = pages_read
        db.session.commit()
        flash(f'Progrès mis à jour : {pages_read} pages lues.', 'success')

    return redirect(url_for('main.index', book_id=book.id))

# DELETE

@bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    db.session.delete(book)
    db.session.commit()
    flash(f'Le livre "{book.title}" a été supprimé.', 'success')
    
    return redirect(url_for('main.index')) 
