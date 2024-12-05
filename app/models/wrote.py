from app.extensions import db
from app.models.author import Author

class Wrote(db.Model):
    __tablename__ = 'wrote'

    isbn = db.Column('ISBN', db.BigInteger, db.ForeignKey('books.ISBN'), primary_key=True)
    author_id = db.Column('idAuthor', db.Integer, db.ForeignKey('authors.idAuthor'), primary_key=True)

    # Relationships
    book = db.relationship('Book', back_populates='authors')
    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        return f'<Auteur "{self.author_id}" wrote "{self.isbn}" >'

    def __init__(self, isbn, id_author):
        self.isbn = isbn
        self.author_id = id_author