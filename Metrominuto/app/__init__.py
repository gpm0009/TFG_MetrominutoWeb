import googlemaps
from flask_googlemaps import GoogleMaps
from config import Config
from flask_bootstrap import Bootstrap
from flask import Flask
# from flask_cors import CORS


bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    # cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
    app.secret_key = Config.SECRET_KEY
    bootstrap.init_app(app)

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    return app
