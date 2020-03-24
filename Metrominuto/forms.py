from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FieldList
from wtforms.validators import DataRequired


class Form(FlaskForm):
    submit = SubmitField('SaveForm')
    number = IntegerField('Votes', validators=[DataRequired()])


class ModeForm(FlaskForm):
    submit = SubmitField('SaveForm')
    choices = [('bicycling', 'Bicicleta'), ('walking', 'A Pie'), ('driving', 'Coche'), ('transit', 'Transporte público')]
    mode = SelectField('Modo', choices=choices)