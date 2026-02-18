from core.extensions import db

authors_books = db.Table('authors_books',
                    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True),
                    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True)
                )

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    books = db.relationship('Book', secondary=authors_books, backref='authors', lazy='dynamic')
