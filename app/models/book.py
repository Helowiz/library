from app.extensions import db
from app.models.saga import Saga
from app.models.wrote import Wrote
from app.models.edition import Edition


class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column('ISBN', db.Integer, primary_key=True)
    title = db.Column('Title', db.String(255), nullable=False, unique=True)
    pages = db.Column('Pages', db.Integer, nullable=False)
    summary = db.Column('Summery', db.Text, nullable=False)
    saga_id = db.Column('idSaga', db.Integer, db.ForeignKey('saga.idSaga'))

    # Relationships
    saga = db.relationship('Saga', back_populates='books')
    authors = db.relationship('Wrote', back_populates='book')
    editions = db.relationship('Edition', back_populates='book')

    def __repr__(self):
        return f'<Book n°"{self.isbn}" "{self.title}">'

    def __init__(self, title, author, pages, summery):
        self.title = title
        self.author = author
        self.pages = pages
        self.summery = summery
