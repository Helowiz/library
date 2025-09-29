from flask import flash

from app.extensions import db

book_kinds = db.Table(
    "book_kinds",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id"), primary_key=True),
    db.Column("kind_id", db.Integer, db.ForeignKey("kind.id"), primary_key=True),
)


class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    synopsis = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), nullable=True, default=None)
    is_favorite = db.Column(db.Boolean, default=False)

    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)
    editions = db.relationship("Edition", backref="book", cascade="all, delete-orphan")
    kinds = db.relationship(
        "Kind",
        secondary=book_kinds,
        lazy="subquery",
        backref=db.backref("books", lazy=True),
    )

    def __repr__(self):
        return f"<Book {self.title}>"

    @classmethod
    def get_favorite_books(cls):
        return cls.query.filter_by(is_favorite=True).all()

    @classmethod
    def search_by_name(cls, title):
        return cls.query.filter(cls.title.ilike(title.strip())).first()

    @classmethod
    def get_or_create(cls, title, author_id, synopsis="", status=None):
        book = cls.search_by_name(title)

        if not book:
            book = cls(
                title=title.strip(),
                synopsis=synopsis,
                author_id=author_id,
                status=status,
            )
            db.session.add(book)
            db.session.commit()
        else:
            flash(f"The book '{title}' already exists.", "warning")

        return book


class Kind(db.Model):
    __tablename__ = "kind"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(
        db.String(150), nullable=False, unique=True
    )  # Ajout de unique=True

    def __repr__(self):
        return f"<Kind {self.name}>"

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name.strip())).first()

    @classmethod
    def get_or_create(cls, name):
        kind = cls.search_by_name(name)

        if not kind:
            kind = cls(name=name.strip())
            db.session.add(kind)
            db.session.commit()

        return name
