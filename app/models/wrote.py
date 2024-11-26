from app.extensions import db
from app.models.author import Author

class Wrote(db.Model):
    __tablename__ = 'wrote'

    isbn = db.Column('ISBN', db.Integer, db.ForeignKey('books.ISBN'), primary_key=True)
    author_id = db.Column('idAuthor', db.Integer, db.ForeignKey('authors.idAuthor'), primary_key=True)

    # Relationships
    book = db.relationship('Book', back_populates='authors')
    author = db.relationship('Author', back_populates='books')