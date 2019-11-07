from flask import Flask, render_template
from flask_googlemaps import GoogleMaps

from datetime import datetime

app = Flask(__name__)

@app.route("/")
def pinta_mapa():
    return render_template(
        "map_template.html"
    )