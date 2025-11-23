from datetime import datetime
from app.extensions import db
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField, FloatField, SelectMultipleField
from wtforms.validators import DataRequired, URL, Length, NumberRange, Optional

import enum

class FormatType(enum.Enum):
    PAPIER = "Papier"
    EBOOK = "Ebook"
    AUDIOBOOK = "Audiobook"

book_tags = db.Table('book_tags',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class Author(db.Model):
    __tablename__ = "author"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    books = db.relationship("Book", back_populates="author")

class Series(db.Model):
    __tablename__ = "series"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    books = db.relationship("Book", back_populates="series")

class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class Quote(db.Model):
    __tablename__ = "quote"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    page_number = db.Column(db.Integer, nullable=True)
    
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    book = db.relationship("Book", back_populates="quotes")

class Book(db.Model):
    __tablename__ = "book"
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(150), nullable=False)
    synopsis = db.Column(db.Text, nullable=True)
    isbn = db.Column(db.String(13), unique=True, nullable=True) 
    cover_url = db.Column(db.String(256), nullable=True)
    publisher = db.Column(db.String(100), nullable=True) 
    language = db.Column(db.String(10), default="FR")
    
    number_of_pages = db.Column(db.Integer, nullable=True)
    format = db.Column(db.Enum(FormatType, native_enum=False), default=FormatType.PAPIER)

    author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)
    author = db.relationship("Author", back_populates="books")

    series_id = db.Column(db.Integer, db.ForeignKey('series.id'), nullable=True)
    series = db.relationship("Series", back_populates="books")
    series_volume = db.Column(db.Float, nullable=True) 
    
    tags = db.relationship('Tag', secondary=book_tags, backref=db.backref('books', lazy='dynamic'))

    readings = db.relationship("ReadingSession", back_populates="book", cascade="all, delete-orphan", order_by="ReadingSession.id.desc()")
    quotes = db.relationship("Quote", back_populates="book")

    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Book {self.title}>"
    
    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.author_id.choices = [(a.id, a.name) for a in Author.query.order_by(Author.name).all()]
        self.series_id.choices = [(0, 'Aucune')] + [(s.id, s.title) for s in Series.query.order_by(Series.title).all()]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]
    
    @classmethod
    def get_book_with_all_data(cls, book_id):
        book = db.session.query(cls).filter_by(id=book_id).first()
        return book
    
    @classmethod
    def find_by_isbn(cls, isbn):
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def find_duplicate(cls, title, author_id, format):
        return cls.query.filter(
            cls.title == title,
            cls.author_id == author_id,
            cls.format == format
        ).first()


class BookForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=150)])
    
    author_id = SelectField('Auteur', coerce=int, validators=[DataRequired()])
    
    series_id = SelectField('Série / Saga', coerce=int, validators=[Optional()])
    series_volume = FloatField('Numéro du tome', validators=[Optional(), NumberRange(min=0)])

    format = SelectField('Format',coerce=FormatType, choices=[
        FormatType.PAPIER.value, 
        FormatType.EBOOK.value, 
        FormatType.AUDIOBOOK.value
    ], validators=[DataRequired()])
    
    language = SelectField('Langue', choices=[
        ('FR', 'Français'), 
        ('EN', 'Anglais'),
    ], default='FR')

    publisher = StringField('Éditeur', validators=[Optional(), Length(max=100)])
    isbn = StringField('ISBN', validators=[Optional(), Length(min=10, max=13)])
    number_of_pages = IntegerField('Nombre de pages', validators=[Optional(), NumberRange(min=1)])

    cover_url = StringField("URL de la couverture", validators=[URL(), Length(max=256)])
    synopsis = TextAreaField('Résumé', validators=[DataRequired()])
    
    tags = SelectMultipleField('Genres', coerce=int)

    submit = SubmitField('Enregistrer le livre')


class DeleteBookForm(FlaskForm):
    submit = SubmitField('Supprimer ce livre')