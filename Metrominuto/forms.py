from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FieldList
from wtforms.validators import DataRequired


class Form(FlaskForm):
    submit = SubmitField('SaveForm')
    number = IntegerField('Votes', validators=[DataRequired()])
    min_votes = IntegerField()
    max_votes = IntegerField()
    value = IntegerField('Votes')


class ModeForm(FlaskForm):
    submit = SubmitField('SaveForm')
    choices = [('bicycling', 'Bicicleta'), ('walking', 'A Pie')]
    mode = SelectField('Modo', choices=choices)