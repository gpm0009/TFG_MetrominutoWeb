from builtins import print

from flask import Flask, render_template, request, jsonify, json
# from flask_googlemaps import GoogleMaps
# from flask_googlemaps import Map, icons
# from googlemaps import convert
from datetime import datetime
import googlemaps
import json
import calculateRoute as clr


app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyBa4H59vDquLKttwMkxv0WaJrx3wXB260s')

@app.route("/", methods=['GET', 'POST'])
def show_map():
    longitude = -3.69
    latitude = 42.34
    # Se puede introducir código de places para cargar directamente el mapa donde queramos.
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude
    )

    # distance_matrix(client, origins, destinations,
    #                 mode=None, language=None, avoid=None, units=None,
    #                 departure_time=None, arrival_time=None, transit_mode=None,
    #                 transit_routing_preference=None, traffic_model=None, region=None);


@app.route("/setMarks", methods=['POST'])
def set_marks():
    place = gmaps.find_place('Burgos', 'textquery')
    print(place)

    markers = request.get_json()
    print(markers)
    origins = []
    destinations = []
    origins.append(markers[0]['position'])
    origins.append(markers[1]['position'])
    destinations.append(markers[2]['position'])
    now = datetime.now()
    # devuelven diccionarios
    origins_prueba = ["Bobcaygeon ON", [41.43206, -81.38992]]
    destinations_prueba = [(43.012486, -83.6964149),
                    {"lat": 42.8863855, "lng": -78.8781627}]

    matrix = gmaps.distance_matrix(origins_prueba, destinations_prueba)

    directions_result = gmaps.directions(markers[0]['position'],
                                         markers[1]['position'],
                                         mode="transit",
                                         departure_time=now)
    print(matrix)
    print(directions_result)
    clr.read_matrix_distance(matrix)
    clr.read_direction(directions_result)
    return render_template("map_template.html")


if __name__ == '__main__':
    app.run()
