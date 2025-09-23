from datetime import datetime

from app.extensions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.DateTime, nullable=True)
    cover_url = db.Column(db.String(250), nullable=True)
    synopsis = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    pages = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(50), nullable=True)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    publisher = db.Column(db.String(100), nullable=True)
    genre = db.Column(db.String(100), nullable=True)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(db.Text, nullable=True)
    is_read = db.Column(db.Boolean, default=False)
    is_favorite = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Book {self.title}>"
