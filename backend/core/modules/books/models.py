from datetime import datetime
from sqlalchemy import Enum
from core.extensions import db

import enum

class FormatType(enum.Enum):
    PAPIER = "Papier"
    EBOOK = "Ebook"
    AUDIOBOOK = "Audiobook"

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True, index=True)
    title = db.Column(db.String(150), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    cover_url = db.Column(db.String(256), nullable=True)
    publisher = db.Column(db.String(100), nullable=True)
    language = db.Column(db.String(10), default="FR")
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    number_of_pages = db.Column(db.Integer, nullable=True)
    format = db.Column(Enum(FormatType, native_enum=False), default=FormatType.PAPIER)

    def __repr__(self):
        return f"<Book {self.title}>"
