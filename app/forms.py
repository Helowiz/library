from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, URL, Length, NumberRange

class BookForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=150)])
    author = StringField('Auteur', validators=[DataRequired(), Length(max=100)])
    url = StringField("URL de la couverture", validators=[URL(), Length(max=256)])
    synopsis = TextAreaField('Résumé', validators=[DataRequired()])
    number_of_pages = IntegerField('Nombre de pages', validators=[DataRequired(), NumberRange(min=1, message="Le nombre de pages doit être supérieur à 0.")])

    submit = SubmitField('Enregistrer le livre')

class DeleteBookForm(FlaskForm):
    pass