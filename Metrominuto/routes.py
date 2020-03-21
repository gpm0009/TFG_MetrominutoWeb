from datetime import datetime
from app import app, google_maps
import calculateRoute as Clr
from flask import render_template, request, session, jsonify, redirect, url_for
from config import Config
import graphs as gph
import svgfunctions as svg_f


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
    # reverse_geocode_result = gmaps.reverse_geocode((40.714224, -73.961452))
    # Contiene latlng de los marcadores del mapa.
    markers = request.get_json()
    origins = []
    destinations = []
    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    now = datetime.now()
    matrix = google_maps.distance_matrix(origins, destinations, mode='walking', departure_time=now)
    dist = Clr.get_distance_matrix_values(matrix)
    votes = gph.calculate_graph(dist, markers, matrix)
    svg_f.generate_svg(votes)
    return redirect(url_for('draw_svg'))


@app.route('/graph', methods=['GET'])
def draw_svg():
    svg = render_template('./grafo_svg.svg')
    return render_template('show_graph.html', svg=svg, API_KEY=Config.GOOGLE_API_KEY)


@app.route("/saveNumber", methods=['POST'])
def save_number():
    num = int(request.get_data())
    graph = gph.connected_graph(num)
    svg_f.generate_svg(graph)
    print(url_for('draw_svg'))
    return redirect(url_for('draw_svg'))


@app.route('/setMode', methods=['POST'])
def set_mode():
    modo = request.form['mode']
    session['mode'] = modo
    if modo:
        return jsonify('OK')
    return jsonify('ERROR')