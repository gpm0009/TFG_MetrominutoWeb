"""
    metrominuto_app.main.forms

    This file contais the forms used by the main module.
"""
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired


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
