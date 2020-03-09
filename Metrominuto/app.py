import googlemaps
from config import Config
import calculateRoute as Clr
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request

app = Flask(__name__)
bootstrap = Bootstrap(app)
google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)


@app.route("/", methods=['GET', 'POST'])
def show_map():
    longitude = -3.69
    latitude = 42.34
    # Se puede introducir código de places para cargar directamente el mapa donde queramos.
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude, API_KEY=Config.GOOGLE_API_KEY
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

    # directions_result = google_maps.directions(markers[0]['position'], markers[1]['position'], mode="transit")
    # print(matrix)
    # print(directions_result)
    dist = Clr.get_distance_matrix_values(matrix)
    Clr.calculate_graph(dist, markers)
    # clr.ejemplo_graph()
    # clr.read_direction(directions_result)
    return render_template('map_template.html', API_KEY=Config.GOOGLE_API_KEY)


@app.route('/prueba')
def draw_svg():
    svg = render_template('./grafo_svg.svg')
    # response = make_response(svg)
    return render_template('prueba.html', svg=svg, API_KEY=Config.GOOGLE_API_KEY)


@app.route("/saveNumber", methods=['POST'])
def save_number():
    num = int(request.get_data())
    Clr.connected_graph(num)
    return render_template('prueba.html', API_KEY=Config.GOOGLE_API_KEY)


if __name__ == '__main__':
    app.run()
