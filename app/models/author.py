from app.extensions import db


class Author(db.Model):
    __tablename__ = "author"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)

    books = db.relationship("Book", backref="author", lazy=True)

    def __repr__(self):
        return f"<Author {self.name}>"

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter(cls.name.ilike(name.strip())).first()

    @classmethod
    def get_or_create(cls, name):
        author = cls.search_by_name(name)
        if not author:
            author = cls(name=name.strip())
            db.session.add(author)
            db.session.commit()
        return author
