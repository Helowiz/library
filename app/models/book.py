from flask import flash

from app.extensions import db
from app.models.author import Author
from app.models.publisher import Edition, Publisher
from sqlalchemy.orm import joinedload 

book_kinds = db.Table(
    "book_kinds",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("kind_id", db.Integer, db.ForeignKey("kind.id"), primary_key=True),
)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    editions = db.relationship("Edition", backref="book", cascade="all, delete-orphan")
    kinds = db.relationship(
        "Kind",
        secondary=book_kinds,
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    state = db.relationship("BookState", backref="book", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Book {self.title}>"

    @classmethod
    def search_by_name(cls, title):
        return cls.query.filter(cls.title.ilike(title.strip())).first()

    @classmethod
    def get_or_create(cls, title, author_id, synopsis="", status=None):
        book = cls.search_by_name(title)

        if not book:
            book = cls(title=title.strip(), synopsis=synopsis, author_id=author_id)
            db.session.add(book)
            db.session.commit()
        else:
            flash(f"The book '{title}' already exists.", "warning")
        return book

    @classmethod
    def get_book_with_all_data(cls, book_id):
        book = (
        db.session.query(cls)
        .options(
            joinedload(cls.author),
            joinedload(cls.editions).joinedload(Edition.publisher),
            joinedload(cls.kinds),
            joinedload(cls.state) 
        )
        .filter(cls.id == book_id)
        .first()
    )
        print(book)
        return book


class BookStatus:
    WISHLIST = "wishlist"
    TO_READ = "to be read"
    READING = "reading"
    READ = "read"

    CHOICES = [TO_READ, READING, READ, WISHLIST]


# Fichier: app/models.py

class BookState(db.Model):
    __tablename__ = "book_state"
    id = db.Column(db.Integer, primary_key=True)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False, unique=True)

    status = db.Column(db.String(50), nullable=False, default=BookStatus.TO_READ)
    current_page = db.Column(db.Integer, default=0)
    is_favorite = db.Column(db.Boolean, default=False)
    
    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)

    @classmethod
    def get_reading_books(cls):
        books = cls.query.filter_by(status=BookStatus.READING).all()
        return books


class Kind(db.Model):
    __tablename__ = "kind"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

    def __repr__(self):
        return f"<Kind {self.name}>"

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name.strip())).first()

    @classmethod
    def get_or_create(cls, name):
        kind = cls.search_by_name(name)

        if not kind:
            kind = cls(name=name.strip())
            db.session.add(kind)
            db.session.commit()

        return kind
