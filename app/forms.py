from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, URL, Length

class BookForm(FlaskForm):
    title = StringField('Titre', validators=[DataRequired(), Length(max=150)])
    author = StringField('Auteur', validators=[DataRequired(), Length(max=100)])
    url = StringField("URL de la couverture", validators=[URL(), Length(max=256)])
    synopsis = TextAreaField('Résumé', validators=[DataRequired()])
    submit = SubmitField('Enregistrer le livre')

class DeleteBookForm(FlaskForm):
    pass