from flask import Flask, render_template, request, jsonify, json
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
#from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def show_map():
    latitude = 42.34
    longitude = -3.69
    if request.method == 'GET':
        return render_template(
            "map_template.html",
            latitud=latitude,
            longitud=longitude
        )
    else:
        markers = request.get_json();
        print(markers[1])
        return render_template("map_route.html",)


@app.route("/show_route", methods=['GET'])
def show_route():

    return 0


# @app.route("/getMarks", methods=['POST'])
# def get_marks():
#     markers = request.args.list('data')
#     #print(markers)
#     return markers


if __name__ == '__main__':
    app.run()
