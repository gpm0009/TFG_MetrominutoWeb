"""
    Metrominuto.routes
    ~~~~~~~~~~~~~~~~~~~~~~~~~
    This file contains the routes of the main module.
"""
from flask_googlemaps import GoogleMaps

from app.main import main
from app.main.forms import Form

import json
from datetime import datetime
from app import calculateRoute as Clr, graphs as gph, svgfunctions as svg_f
from flask import render_template, request, session, jsonify, redirect, url_for
from config import Config


google_maps = GoogleMaps(key=Config.GOOGLE_API_KEY)


@main.route("/", methods=['GET', 'POST'])
def show_map():
    """
    Set map center into a specif location (Burgos:[lat:42.34, lng:-3.69]).

    :return:
            Reditect to Maps.
    """
    longitude = -3.69
    latitude = 42.34
    # Se puede introducir código de places para cargar directamente el mapa donde queramos.
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude, API_KEY=Config.GOOGLE_API_KEY
    )


@main.route("/setMarks", methods=['POST'])
def set_marks():
    """
    Save markers from the request and calculate matrix distance between all connections.

    :return:
            Rendered graph view.
    """
    # Contiene latlng de los marcadores del mapa.
    # markers = request.get_json()
    # with open('marcadores.json', 'w') as outfile:
    #     json.dump(markers, outfile)
    with open('../static/marcadores.json') as markers_file:
        new_markers = json.load(markers_file)
    markers = []
    for element in new_markers:
        markers.append({'position': element})
    origins = []
    destinations = []
    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    now = datetime.now()
    # matrix = google_maps.distance_matrix(origins, destinations, mode=session['mode'], departure_time=now)
    # with open('distance_matrix.json', 'w') as outfile_matrix:
    #     json.dump(matrix, outfile_matrix)
    with open('../static/distance_matrix.json') as matrix_file:
        matrix = json.load(matrix_file)
    dist = Clr.get_distance_matrix_values(matrix)
    votes = gph.calculate_graph(dist, markers, matrix)
    svg_f.generate_svg(votes)
    return redirect(url_for('main.draw_svg'))


@main.route('/graph', methods=['GET', 'POST'])
def draw_svg():
    """
    Save number of edges votes that user want to see in the graph.

    :return:
            Rendered graph view.
    """
    form = Form()
    svg = None
    if form.validate_on_submit():
        num = form.number.data
        graph = gph.connected_graph(num)
        svg_f.generate_svg(graph)
        return redirect(url_for('main.draw_svg'))
    elif request.method == 'GET':
        # form.max_votes = session['max_votes']
        # form.min_votes = session['min_votes']
        form.max_votes = 25
        form.min_votes = 0
        svg = render_template('./grafo_svg.svg')
    return render_template('show_graph.html', form=form, svg=svg)


# @app.route("/saveNumber", methods=['POST', 'GET'])
# def save_number():
#     num = int(request.get_data())
#     graph = gph.connected_graph(num)
#     svg_f.generate_svg(graph)
#     return redirect(url_for('main.draw_svg'))

# @app.route('/setMode', methods=['POST'])
# def set_mode():
#     mode_form = ModeForm()
#     if mode_form.validate_on_submit():
#         num = mode_form.number.data
#         mode = mode_form.mode.data
#     return render_template('map_template.html', form=mode_form)


@main.route('/setMode', methods=['POST'])
def set_mode():
    """
    Save travel mode (walking or cycling) in order to calculate times and distances.

    :return:
            JSON message.
    """
    mode = request.form['mode']
    session['mode'] = mode
    if mode:
        return jsonify('OK')
    return jsonify('ERROR')


@main.route('/api/mensaje')
def mensaje():
    return render_template('vue_template.html')

