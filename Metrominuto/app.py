import googlemaps
from config import Config
import calculateRoute as Clr
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

app = Flask(__name__)
bootstrap = Bootstrap(app)
google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)

import routes