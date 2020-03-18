import googlemaps
from config import Config
from flask_bootstrap import Bootstrap
from flask import Flask, session

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY
bootstrap = Bootstrap(app)
google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)

import routes