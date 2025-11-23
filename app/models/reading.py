import enum
from app.extensions import db


class ReadingStatus(enum.Enum):
    DNF = "Do Not Finish"
    PAUSE = "Pause"
    WISHLIST = "Wishlist"
    TBR = "To Be read"
    READING = "Reading"
    READ = "Read"


class ReadingSession(db.Model):
    __tablename__ = "reading_session"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book = db.relationship("Book", back_populates="readings")

    status = db.Column(db.Enum(ReadingStatus), default=ReadingStatus.TBR)

    start_date = db.Column(db.Date, nullable=True)
    finish_date = db.Column(db.Date, nullable=True)

    current_page = db.Column(db.Integer, default=0)

    rating = db.Column(db.Integer, nullable=True)
    review = db.Column(db.Text, nullable=True)

    is_reread = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Reading {self.book.title} - {self.status.value}>"
