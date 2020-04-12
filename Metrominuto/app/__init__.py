"""
    app

    Web application to automate the process of creating synoptics map,
    metrominutos
"""
import googlemaps
from config import Config
from flask_bootstrap import Bootstrap
from flask import Flask


bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.secret_key = Config.SECRET_KEY
    bootstrap.init_app(app)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    return app
