from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField,
    IntegerField,
    SelectField,
    FloatField,
    SelectMultipleField,
)
from wtforms.validators import DataRequired, URL, Length, NumberRange, Optional
from app.models.book import FormatType, Author, Series, Tag 

class BookForm(FlaskForm):
    title = StringField("Titre", validators=[DataRequired(), Length(max=150)])
    author_id = SelectField("Auteur", coerce=int, validators=[DataRequired()])
    series_id = SelectField("Série / Saga", coerce=int, validators=[Optional()])
    series_volume = FloatField(
        "Numéro du tome", validators=[Optional(), NumberRange(min=0)]
    )

    format = SelectField(
        "Format",
        coerce=FormatType,
        choices=[
            FormatType.PAPIER.value,
            FormatType.EBOOK.value,
            FormatType.AUDIOBOOK.value,
        ],
        validators=[DataRequired()],
    )

    language = SelectField(
        "Langue",
        choices=[
            ("FR", "Français"),
            ("EN", "Anglais"),
        ],
        default="FR",
    )

    publisher = StringField("Éditeur", validators=[Optional(), Length(max=100)])
    isbn = StringField("ISBN", validators=[Optional(), Length(min=10, max=13)])
    number_of_pages = IntegerField(
        "Nombre de pages", validators=[Optional(), NumberRange(min=1)]
    )
    cover_url = StringField("URL de la couverture", validators=[URL(), Length(max=256)])
    synopsis = TextAreaField("Résumé", validators=[DataRequired()])
    tags = SelectMultipleField("Genres", coerce=int)
    submit = SubmitField("Enregistrer le livre")

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)        
        self.author_id.choices = [
            (a.id, a.name) for a in Author.query.order_by(Author.name).all()
        ]
        self.series_id.choices = [(0, "Aucune")] + [
            (s.id, s.title) for s in Series.query.order_by(Series.title).all()
        ]
        self.tags.choices = [(t.id, t.name) for t in Tag.query.order_by(Tag.name).all()]

class DeleteBookForm(FlaskForm):
    submit = SubmitField("Supprimer ce livre")
