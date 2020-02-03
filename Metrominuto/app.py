from flask import Flask, render_template, request, jsonify, json, redirect
import googlemaps
import calculateRoute as clr
from flask_bootstrap import Bootstrap

app = Flask(__name__)
bootstrap = Bootstrap(app)
google_maps = googlemaps.Client(key='')


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
    matrix = google_maps.distance_matrix(origins, destinations)

    # directions_result = gmaps.directions(markers[0]['position'], markers[1]['position'], mode="transit")
    # print(matrix)
    # print(directions_result)
    dist = clr.get_distance_matrix_values(matrix)
    clr.draw_graph(dist, markers)
    # clr.read_direction(directions_result)
    grafo()
    return render_template('map_template.html')


@app.route('/graph', methods=['GET', 'POST'])
def grafo():

    return render_template('tubemap.html')


if __name__ == '__main__':
    app.run()
