from datetime import datetime

from app.extensions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    published_date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    cover_url = db.Column(db.String(250), nullable=True)

    def __repr__(self):
        return f"<Book {self.title}>"
