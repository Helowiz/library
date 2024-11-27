from app.extensions import db


class Saga(db.Model):
    __tablename__ = 'saga'

    id = db.Column('idSaga', db.Integer, primary_key=True)
    name = db.Column('NameSaga', db.String(255), nullable=False, unique=True)
    number_of_volumes = db.Column('NumberOfVolumes', db.Integer, nullable=False)

    # Relationships
    books = db.relationship('Book', back_populates='saga')

    def __repr__(self):
        return f'<Saga "{self.id}" "{self.saga}" in "{self.number_of_volumes}" volumes >'

    def __init__(self, name, volumes):
        self.name = name
        self.number_of_volumes = volumes