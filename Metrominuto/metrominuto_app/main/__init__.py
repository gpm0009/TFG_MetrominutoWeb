"""
    metrominuto_app.main

    Main module of the application.
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from metrominuto_app.main import routes
