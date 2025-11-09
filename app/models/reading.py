import enum
from datetime import datetime
from app.extensions import db

class BookStatus(enum.Enum):
    WISHLIST = "Wishlist"
    TBR = "To Be read"
    READING = "Reading"
    READ = "Read"

class Reading(db.Model):
    __tablename__ = "reading"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False, unique=True)
    status = db.Column(db.Enum(BookStatus), nullable=True)
    current_page = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    book = db.relationship("Book", back_populates="reading_status")

    def __repr__(self):
        return f"<Reading {self.book.title} - {self.status.value}>"