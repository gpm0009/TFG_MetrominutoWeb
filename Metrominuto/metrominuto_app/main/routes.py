"""
    metrominuto_app.main.routes

    This file contains the routes of the main module.
"""
import json
from datetime import datetime
from metrominuto_app import svgfunctions as svg_f, graphs as gph, calculateRoute as Clr
from flask import render_template, request, session, jsonify, redirect, url_for
from config import Config
from metrominuto_app.main.forms import Form, ModeForm
import googlemaps
from metrominuto_app.main import main
import os

google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)


@main.route("/", methods=['GET', 'POST'])
def show_map():
    longitude = -3.69
    latitude = 42.34
    with open('metrominuto_app/static/markers_example1.json') as markers_file:
        new_markers = json.load(markers_file)
    markers = []
    for element in new_markers:
        markers.append(element)
    # Se puede introducir código de places para cargar directamente el mapa donde queramos.
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude, API_KEY=Config.GOOGLE_API_KEY, positions=json.dumps(markers)
    )


@main.route("/setMarks", methods=['POST'])
def set_marks():
    # Contiene latlng de los marcadores del mapa.
    markers_aux = request.get_json()
    markers = markers_aux['marcadores']
    central_markers = markers_aux['centrales']
    # with open('static/markers_example1.json', 'w') as outfile:
    #     json.dump(markers, outfile)
    with open('metrominuto_app/static/markers_example1.json') as markers_file:
        new_markers = json.load(markers_file)
    markers = []
    for element in new_markers:
        markers.append(element)
    origins = []
    destinations = []
    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    now = datetime.now()
    # matrix = google_maps.distance_matrix(origins, destinations, mode=session['mode'], departure_time=now)
    # with open('static/distance_matrix_example1.json', 'w') as outfile_matrix:
    #     json.dump(matrix, outfile_matrix)
    with open('metrominuto_app/static/distance_matrix_example1.json') as matrix_file:
        matrix = json.load(matrix_file)

    dist = Clr.get_distance_matrix_values(matrix)
    votes = gph.calculate_graph(dist, markers, central_markers, matrix)
    svg_f.generate_svg(votes)
    session['votes_number'] = -1
    return redirect(url_for('main.draw_svg'))

# @main.route("/setMarks", methods=['GET', 'POST'])
# def set_marks():
#     # with open('static/markers_example1.json', 'w') as outfile:
#     #     json.dump(markers, outfile)
#     with open('metrominuto_app/static/markers_example1.json') as markers_file:
#         new_markers = json.load(markers_file)
#     markers = []
#     for element in new_markers:
#         markers.append(element)
#     origins = []
#     destinations = []
#     for mark in markers:
#         origins.append(mark['position'])
#         destinations.append(mark['position'])
#
#     form_mode = ModeForm()
#     if form_mode.validate_on_submit():
#         mode = form_mode.number.data
#         markers_aux = request.get_json()
#         #markers = markers_aux['marcadores']
#         # central_markers = markers_aux['centrales']
#         now = datetime.now()
#         # matrix = google_maps.distance_matrix(origins, destinations, mode=session['mode'], departure_time=now)
#         # with open('static/distance_matrix_example1.json', 'w') as outfile_matrix:
#         #     json.dump(matrix, outfile_matrix)
#         with open('metrominuto_app/static/distance_matrix_example1.json') as matrix_file:
#             matrix = json.load(matrix_file)
#         dist = Clr.get_distance_matrix_values(matrix)
#         votes = gph.calculate_graph(dist, markers, central_markers, matrix)
#         svg_f.generate_svg(votes)
#         return redirect(url_for('main.draw_svg'))
#     longitude = -3.69
#     latitude = 42.34
#     return render_template(
#         'map_template.html',
#         longitude=longitude,
#         latitude=latitude, API_KEY=Config.GOOGLE_API_KEY, positions=json.dumps(markers), form=form_mode)


@main.route('/graph', methods=['GET', 'POST'])
def draw_svg():
    form = Form()
    svg = None
    if request.method == 'POST':
        form.number = int(request.form['num'])
        session['votes_number'] = form.number
        graph = gph.connected_graph(form.number)
        svg_f.generate_svg(graph)
        # return redirect(url_for('main.draw_svg'))
    elif request.method == 'GET':
        form.max_votes = session['max_votes']
        form.min_votes = session['min_votes']
        if session['votes_number'] != -1:
            form.number = session['votes_number']
        else:
            form.number = form.min_votes
        svg = render_template('./grafo_svg.svg')
    return render_template('show_graph.html', form=form, svg=svg)


# @metrominuto_app.route("/saveNumber", methods=['POST', 'GET'])
# def save_number():
#     num = int(request.get_data())
#     graph = gph.connected_graph(num)
#     svg_f.generate_svg(graph)
#     return redirect(url_for('draw_svg'))

# @metrominuto_app.route('/setMode', methods=['POST'])
# def set_mode():
#     mode_form = ModeForm()
#     if mode_form.validate_on_submit():
#         num = mode_form.number.data
#         mode = mode_form.mode.data
#     return render_template('map_template.html', form=mode_form)


@main.route('/setMode', methods=['POST'])
def set_mode():
    mode = request.form['mode']
    session['mode'] = mode
    if mode:
        return jsonify('OK')
    return jsonify('ERROR')


@main.route('/api/mensaje')
def mensaje():
    return render_template('vue_template.html')

