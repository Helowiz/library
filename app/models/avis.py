from app.extensions import db


class Opinion(db.Model):
    __tablename__ = "opinion"

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Float, nullable=True)
    review = db.Column(db.Text, nullable=True)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    book = db.relationship(
        "Book", foreign_keys=[book_id], backref=db.backref("opinions", lazy=True)
    )

    def __repr__(self):
        return f"<Opinion {self.id}>"
