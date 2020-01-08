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
    # place = gmaps.find_place('Burgos', 'textquery')
    # Contiene latlng de los marcadores del mapa.
    markers = request.get_json()
    origins = []
    destinations = []

    # Burgos = 42.34, -3.69
    # Medina = 42.93, -3.51
    # Villar = 42.9396796, -3.5805516
    # Espinosa = 43.0792415, -3.5550065
    # origins_prueba = [[42.34, -3.69], [42.93, -3.51], [42.9396796, -3.5805516], [43.0792415, -3.5550065]]
    # destinations_prueba = [[42.34, -3.69], [42.93, -3.51], [42.9396796, -3.5805516], [43.0792415, -3.5550065]]
    # matrix = gmaps.distance_matrix(origins_prueba, destinations_prueba)
    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    matrix = gmaps.distance_matrix(origins, destinations)

    # directions_result = gmaps.directions(markers[0]['position'],
    #                                      markers[1]['position'],
    #                                      mode="transit")
    # print(matrix)
    # print(directions_result)
    clr.get_distance_matrix_values(matrix)
    # clr.read_direction(directions_result)
    return render_template("map_template.html")



if __name__ == '__main__':
    app.run()
