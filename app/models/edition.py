from app.extensions import db
from app.models.publisher import Publisher

class Edition(db.Model):
    __tablename__ = 'edition'

    isbn = db.Column('ISBN', db.BigInteger, db.ForeignKey('books.ISBN'), primary_key=True)
    publisher_id = db.Column('idPublisher', db.Integer, db.ForeignKey('publisher.idPublisher'), primary_key=True)
    price = db.Column('PriceEdition', db.Float, nullable=False)
    year = db.Column('YearEdition', db.Date, nullable=False)

    # Relationships
    book = db.relationship('Book', back_populates='editions')
    publisher = db.relationship('Publisher', back_populates='editions')

    def __repr__(self):
        return f'<Edition ISBN["{self.isbn}"] | "{self.price}" euros | "{self.year}">'

    def __init__(self, isbn, id_publisher, price, year_edition):
        self.isbn = isbn
        self.publisher_id = id_publisher
        self.price = price
        self.year = year_edition