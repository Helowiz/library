from app.extensions import db
import enum

class SeriesStatus(enum.Enum):
    ONGOING = "En cours"
    FINISHED = "Terminé"
    ABANDONED = "Abandonné"

class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    nb_of_volumes = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Enum(SeriesStatus), default=SeriesStatus.ONGOING)
    books = db.relationship("Book", back_populates="series")

    @classmethod
    def get_books(cls, series_id):
        series = cls.query.get(series_id)
        if series:
            return sorted(series.books, key=lambda book: book.series_volume or 0)
        return []
