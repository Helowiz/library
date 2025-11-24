from datetime import datetime
from app.extensions import db

import enum


class FormatType(enum.Enum):
    PAPIER = "Papier"
    EBOOK = "Ebook"
    AUDIOBOOK = "Audiobook"


class SeriesStatus(enum.Enum):
    ONGOING = "En cours"
    FINISHED = "Terminé"
    ABANDONED = "Abandonné"


book_tags = db.Table(
    "book_tags",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("tag_id", db.Integer, db.ForeignKey("tag.id"), primary_key=True),
)


class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship("Book", back_populates="author")


class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    nb_of_volumes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(SeriesStatus), default=SeriesStatus.ONGOING)
    books = db.relationship("Book", back_populates="series")


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)


class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    page_number = db.Column(db.Integer, nullable=True)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book = db.relationship("Book", back_populates="quotes")


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    cover_url = db.Column(db.String(256), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default="FR")
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_pages = db.Column(db.Integer, nullable=True)
    format = db.Column(db.Enum(FormatType, native_enum=False), default=FormatType.PAPIER)
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    series_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=True)
    series_volume = db.Column(db.Float, nullable=True)

    author = db.relationship("Author", back_populates="books")
    series = db.relationship("Series", back_populates="books")
    tags = db.relationship("Tag", secondary=book_tags, backref=db.backref("books", lazy="dynamic"))
    quotes = db.relationship("Quote", back_populates="book")
    readings = db.relationship(
        "ReadingSession",
        back_populates="book",
        cascade="all, delete-orphan",
        order_by="ReadingSession.id.desc()",
    )


    def __repr__(self):
        return f"<Book {self.title}>"

    @classmethod
    def get_book_with_all_data(cls, book_id):
        book = db.session.query(cls).filter_by(id=book_id).first()
        return book

    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def find_duplicate(cls, title, author_id, format):
        return cls.query.filter(
            cls.title == title, cls.author_id == author_id, cls.format == format
        ).first()
