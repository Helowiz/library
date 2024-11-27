from app.extensions import db

class Publisher(db.Model):
    __tablename__ = 'publisher'

    id = db.Column('idPublisher', db.Integer, primary_key=True)
    name = db.Column('NamePublisher', db.String(255), nullable=False, unique=True)
    language = db.Column('LangageEdition', db.String(50), nullable=False)

    # Relationships
    editions = db.relationship('Edition', back_populates='publisher')

    def __repr__(self):
        return f'<Publisher n° "{self.id}" "{self.name}" >'

    def __init__(self, name, language):
        self.name = name
        self.language = language
