"""
    metrominuto_app

    Web application to automate the process of creating synoptics map,
    metrominutos
"""
# import googlemaps
from config import Config
from flask_bootstrap import Bootstrap
from flask import Flask
import os
import config

bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    config_name = os.environ.get('ENVIRONMENT') or 'default'
    # app.secret_key = Config.SECRET_KEY
    app.config.from_object(config.config[config_name])
    bootstrap.init_app(app)

    from metrominuto_app.main import main as main_bp
    app.register_blueprint(main_bp)

    return app


app = create_app()
