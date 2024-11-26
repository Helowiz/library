from app.extensions import db


class Author(db.Model):
    __tablename__ = 'authors'

    id = db.Column('idAuthor', db.Integer, primary_key=True)
    name = db.Column('NameAuthor', db.String(255), nullable=False)

    # Relationships
    books = db.relationship('Wrote', back_populates='author')

    def __repr__(self):
        return f'<Author "{self.id}" "{self.name}" >'

    def __init__(self, name):
        self.nameAuthor = name

