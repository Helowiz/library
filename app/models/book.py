from flask import flash
from datetime import datetime
from app.extensions import db
from app.models.reading import Reading, BookStatus

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    cover_url = db.Column(db.String(256), nullable=False)
    number_of_pages = db.Column(db.Integer, nullable=True)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    reading_status = db.relationship("Reading", back_populates="book", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title}>"
    
    @classmethod
    def search_by_name(cls, title):
        return db.session.query(cls).filter_by(title=title.strip()).first()

    @classmethod
    def get_or_create(cls, title, author, synopsis="", url="", number_of_pages=0, status=None, current_page=0):
        book = cls.search_by_name(title)
        if not book:
            book = cls(title=title.strip(), synopsis=synopsis, author=author, cover_url=url, number_of_pages=number_of_pages)

            page = current_page if status == BookStatus.READING else None

            reading = Reading(status=status, current_page=page)
            book.reading_status = reading

            db.session.add(book)
            db.session.commit()
            flash(f"The book '{title}' has been created successfully.", "success")
        else:
            flash(f"The book '{title}' already exists.", "warning")
        return book

    @classmethod
    def get_book_with_all_data(cls, book_id):
        book = db.session.query(cls).filter_by(id=book_id).first()
        return book
