from app.extensions import db
from app.models.publisher import Publisher

class Edition(db.Model):
    __tablename__ = 'edition'

    isbn = db.Column('ISBN', db.Integer, db.ForeignKey('books.ISBN'), primary_key=True)
    publisher_id = db.Column('idPublisher', db.Integer, db.ForeignKey('publisher.idPublisher'), primary_key=True)
    year = db.Column('YearEdition', db.Date, nullable=False)

    # Relationships
    book = db.relationship('Book', back_populates='editions')
    publisher = db.relationship('Publisher', back_populates='editions')