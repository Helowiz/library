from flask import flash, redirect, render_template, url_for, abort, request

from app.book import bp
from app.extensions import db
from app.models.book import Book, Author, Series, Tag, BookForm, DeleteBookForm 
from app.models.reading import ReadingStatus, ReadingSession

# READ
@bp.route("/")
def list_books():
    status_filter = request.args.get('status') 
    search_query = request.args.get('q')

    query = db.session.query(Book).outerjoin(ReadingSession)

    if status_filter and status_filter in ReadingStatus.__members__:
        query = query.filter(ReadingSession.status == ReadingStatus[status_filter])
    
    if search_query:
        query = query.filter(Book.title.ilike(f"%{search_query}%"))

    query = query.group_by(Book.id)
    books = query.all()
    
    return render_template("book/list.html", 
                           books=books, 
                           current_status=status_filter,
                           ReadingStatus=ReadingStatus)


@bp.route("/<int:book_id>")
def detail_book(book_id):
    delete_form = DeleteBookForm()
    book = Book.query.get_or_404(book_id)

    latest_session = None
    if book.readings:
        latest_session = book.readings[0]

    if latest_session:
        print(f"Le statut actuel est : {latest_session.status.value}")
    else:
        print("Ce livre n'a pas encore de session de lecture.")

    return render_template(
        "book/detail.html", 
        book=book, 
        latest_session=latest_session,
        delete_form=delete_form, 
        ReadingStatus=ReadingStatus
    )
# CREATE

@bp.route('/add', methods=['GET', 'POST'])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        if form.isbn.data and (book := Book.find_by_isbn(form.isbn.data)):
            flash(f"Ce livre existe déjà (ISBN identique) : {book.title}", "warning")
            return redirect(url_for('book.detail_book', book_id=book.id))

        if (book := Book.find_duplicate(form.title.data, form.author_id.data, form.format.data)):
            flash(f"Tu possèdes déjà '{book.title}' dans ce format !", "warning")
            return redirect(url_for('book.detail_book', book_id=book.id))

        try:
            new_book = Book()
            form.populate_obj(new_book)
            new_book.series_id = form.series_id.data if form.series_id.data != 0 else None
            if form.tags.data:
                new_book.tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()

            db.session.add(new_book)
            db.session.commit()
            flash("Livre ajouté avec succès !", "success")
            return redirect(url_for('book.detail_book', book_id=new_book.id))

        except Exception as e:
            db.session.rollback()
            flash(f"Erreur technique : {str(e)}", "danger")
            print(e)

    return render_template('book/add.html', form=form, button_text="Ajouter le livre")

# UPDATE

@bp.route('/edit/<int:book_id>/', methods=['GET', 'POST'])
def update_book(book_id):
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

    if status_key in ReadingStatus.__members__:
        new_status = ReadingStatus[status_key]

        latest_session = book.readings[0] if book.readings else None

        if latest_session is None:
            new_session = ReadingSession(book=book, status=new_status)
            db.session.add(new_session)
            flash(f'Lecture commencée avec le statut : "{new_status.value}"', 'success')
        else:
            latest_session.status = new_status
            flash(f'Le statut du livre a été mis à jour : "{new_status.value}"', 'success')
        
        db.session.commit()
    
    else:
        flash('Statut non valide.', 'danger')

    return redirect(url_for('book.detail_book', book_id=book.id))

@bp.route('/book/<int:book_id>/progress', methods=['POST'])
def update_progress(book_id):
    book = Book.query.get_or_404(book_id)
    try:
        pages_read = int(request.form.get('pages_read', 0))
    except (ValueError, TypeError):
        flash('Veuillez entrer un nombre valide de pages lues.', 'danger')
        return redirect(url_for('book.detail_book', book_id=book.id))

    if book.number_of_pages and (pages_read < 0 or pages_read > book.number_of_pages):
        flash('Le nombre de pages lues doit être entre 0 et le nombre total de pages du livre.', 'danger')
        return redirect(url_for('book.detail_book', book_id=book.id))

    latest_session = book.readings[0] if book.readings else None

    if latest_session is None:
        latest_session = ReadingSession(book=book, current_page=pages_read)
        db.session.add(latest_session)
    else:
        latest_session.current_page = pages_read
    
    db.session.commit()
    flash(f'Progrès mis à jour : {pages_read} pages lues.', 'success')
    return redirect(url_for('book.detail_book', book_id=book.id))

# DELETE

@bp.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    
    db.session.delete(book)
    db.session.commit()
    flash(f'Le livre "{book.title}" a été supprimé.', 'success')
    
    return redirect(url_for('main.index')) 
