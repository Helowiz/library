from app.extensions import db

class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    page_number = db.Column(db.Integer, nullable=True)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book = db.relationship("Book", back_populates="quotes")

