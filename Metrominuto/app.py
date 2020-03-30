import googlemaps
from config import Config
from flask_bootstrap import Bootstrap
from flask import Flask
from flask_cors import CORS


# app = Flask(__name__,
#             static_folder='./frontend/dist/static',
#             template_folder='./frontend/dist')

# cors = CORS(app, resources={r'/api/*': {'origins': '*'}})
app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
bootstrap = Bootstrap(app)
google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)

import routes