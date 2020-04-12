"""
    app.main.forms

    This file contais the forms used by the main module.
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField, FieldList
from wtforms.validators import DataRequired


class Form(FlaskForm):
    """Form to handle the change of votes in the synoptic map.

    :Attributes
    submit: SubmitField
        Input field of type submit to trigger the upload action.
    number: IntegerField
        Field containing the number of votes in the edges graph.
    min_votes: IntegerField
        Field containing the minimum number in the votes matrix.
    max_votes: IntegerField
        Field containing the maximum number in the votes matrix.

    """
    submit = SubmitField('SaveForm')
    number = IntegerField('Votes', validators=[DataRequired()])
    min_votes = IntegerField()
    max_votes = IntegerField()
    value = IntegerField()


class ModeForm(FlaskForm):
    """Form that handles route type selection.

    :Attributes
    submit: SubmitField
        Input field of type submit to trigger the upload action.
    mode: SelectField
        Field containing possible route types.

    """
    submit = SubmitField('SaveForm')
    mode = SelectField('Modo', choices=[('bicycling', 'Bicicleta'), ('walking', 'A Pie')])