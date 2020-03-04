import io
import random

import networkx as nx
from flask import Flask, render_template, request, jsonify, json, redirect, Response, make_response
import googlemaps
from markupsafe import Markup
from matplotlib.backends.backend_svg import FigureCanvasSVG
from matplotlib.figure import Figure

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
    clr.calculate_graph(dist, markers)
    # clr.ejemplo_graph()
    # clr.read_direction(directions_result)
    return render_template('map_template.html')

@app.route('/grafo')
def plot_svg(num_x_points=50):
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    x_points = range(num_x_points)
    axis.plot(x_points, [random.randint(1, 30) for x in x_points])

    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return Response(output.getvalue(), mimetype="image/svg+xml")


@app.route('/prueba')
def draw_svg():
    svg = render_template('./grafo_svg.svg')
    # response = make_response(svg)
    return render_template('prueba.html', svg=svg)


if __name__ == '__main__':
    app.run()
