from flask import flash

from app.extensions import db

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"<Book {self.title}>"
    
    @classmethod
    def search_by_name(cls, title):
        return db.session.query(cls).filter_by(title=title.strip()).first()

    @classmethod
    def get_or_create(cls, title, author, synopsis="", url=""):
        book = cls.search_by_name(title)
        if not book:
            book = cls(title=title.strip(), synopsis=synopsis, author=author, url=url)
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
