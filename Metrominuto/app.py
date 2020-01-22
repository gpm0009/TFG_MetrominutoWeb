from builtins import print

from flask import Flask, render_template, request, jsonify, json, redirect
from datetime import datetime
import googlemaps
import calculateRoute as clr
import random
import networkx as nx
import matplotlib.pyplot as plt

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

    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    matrix = gmaps.distance_matrix(origins, destinations)

    # directions_result = gmaps.directions(markers[0]['position'],
    #                                      markers[1]['position'],
    #                                      mode="transit")
    # print(matrix)
    # print(directions_result)
    dist = clr.get_distance_matrix_values(matrix)
    clr.draw_graph(dist, markers)
    # clr.read_direction(directions_result)
    return render_template('map_template.html')


# @app.route('/graph', methods=['GET'])
# def grafo():
#
#     return render_template('graph.html')


if __name__ == '__main__':
    app.run()
