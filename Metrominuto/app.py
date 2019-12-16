from builtins import print

from flask import Flask, render_template, request, jsonify, json
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from googlemaps import convert
from datetime import datetime
import googlemaps
import json

app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyBa4H59vDquLKttwMkxv0WaJrx3wXB260s')

@app.route("/", methods=['GET', 'POST'])
def show_map():
    latitude = 42.34
    longitude = -3.69
    coordenadas=[]
    if request.method == 'GET':
        return render_template(
            "map_template.html",
            latitud=latitude,
            longitud=longitude
        )
    else:
        markers = []
        markers = request.get_json();
        # for mark in markers:
        #     al = convert.latlng(mark)
        #     print(al)
        #     coordenadas.append(al)
        print(markers)
        show_route(coordenadas)
        return render_template("map_route.html")


@app.route("/show_route", methods=['GET'])
def show_route(coordenadas):
    # Look up an address with reverse geocoding
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    # print(reverse_geocode_result)
    # Request directions via public transit
    now = datetime.now()
    # directions_result = gmaps.directions("Sydney Town Hall",
    #                                      "Parramatta, NSW",
    #                                      mode="transit",
    #                                      departure_time=now)

    return 0


# @app.route("/getMarks", methods=['POST'])
# def get_marks():
#     markers = request.args.list('data')
#     #print(markers)
#     return markers


if __name__ == '__main__':
    app.run()
