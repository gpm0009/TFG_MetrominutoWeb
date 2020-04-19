"""
    metrominuto_app.main.forms

    This file contais the forms used by the main module.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
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
    submit = SubmitField('Sign In')
    number = IntegerField('Number of votes:')
    min_votes = IntegerField()
    max_votes = IntegerField()


class MapForm(FlaskForm):
    """Form that handles route type selection.

    :Attributes
    submit: SubmitField
        Input field of type submit to trigger the upload action.
    mode: SelectField
        Field containing possible route types.

    """
    submit = SubmitField('Mostrar Mapa')
    mode = SelectField('Tipo de ruta: ', choices=[('bicycling', 'Bicicleta'), ('walking', 'A Pie')])
