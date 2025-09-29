from app.extensions import db


class Publisher(db.Model):
    __tablename__ = "publisher"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)

    editions = db.relationship("Edition", backref="publisher")

    def __repr__(self):
        return f"<Publisher {self.title}>"

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name.strip())).first()

    @classmethod
    def get_or_create(cls, name):
        if not name:
            return None
        publisher = cls.search_by_name(name)
        if not publisher:
            publisher = cls(name=name.strip())
            db.session.add(publisher)
            db.session.commit()
        return publisher


class Edition(db.Model):
    __tablename__ = "edition"

    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(20), nullable=True, unique=True)
    published_date = db.Column(db.DateTime, nullable=True)
    cover_url = db.Column(db.String(250), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    language = db.Column(db.String(50), nullable=True)

    book_id = db.Column(db.Integer, db.ForeignKey("book.id"), nullable=False)
    publisher_id = db.Column(db.Integer, db.ForeignKey("publisher.id"), nullable=False)

    def __repr__(self):
        return f"<Edition {self.isbn}>"

    @classmethod
    def search_by_isbn(cls, isbn):
        return cls.query.filter(cls.isbn.ilike(isbn.strip())).first()

    @classmethod
    def get_or_create(
        cls,
        isbn,
        published_date=None,
        cover_url=None,
        pages=None,
        language=None,
        book=None,
        publisher=None,
    ):
        edition = cls.search_by_isbn(isbn)
        if not edition:
            edition = cls(
                isbn=isbn.strip(),
                published_date=published_date,
                cover_url=cover_url,
                pages=pages,
                language=language,
                book=book,
                publisher=publisher,
            )
            db.session.add(edition)
            db.session.commit()
        return edition
