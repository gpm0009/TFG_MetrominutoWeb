from flask import Flask, render_template, request, jsonify, json, redirect, Response
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
    clr.calculate_graph(dist, markers)
    # clr.ejemplo_graph()
    # clr.read_direction(directions_result)
    return render_template('map_template.html')


@app.route('/prueba')
def draw_svg():
    svg = render_template('./grafo_svg.svg')
    # response = make_response(svg)
    return render_template('prueba.html', svg=svg)


@app.route("/saveNumber", methods=['POST'])
def save_number():
    num = int(request.get_data())
    clr.conected_graph(num)
    return render_template('prueba.html')


if __name__ == '__main__':
    app.run()
