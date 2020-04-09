import json
from datetime import datetime
from app import app, google_maps
import calculateRoute as Clr
from flask import render_template, request, session, jsonify, redirect, url_for, flash
from config import Config
import graphs as gph
import svgfunctions as svg_f
from forms import Form, ModeForm


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
    # Contiene latlng de los marcadores del mapa.
    markers = request.get_json()
    with open('./static/marcadores.json', 'w') as outfile:
        json.dump(markers, outfile)
    # with open('./static/marcadores.json') as markers_file:
    #     new_markers = json.load(markers_file)
    # markers = []
    # for element in new_markers:
    #     markers.append({'position': element})
    origins = []
    destinations = []
    for mark in markers:
        origins.append(mark['position'])
        destinations.append(mark['position'])
    now = datetime.now()
    matrix = google_maps.distance_matrix(origins, destinations, mode=session['mode'], departure_time=now)
    with open('./static/distance_matrix.json', 'w') as outfile_matrix:
        json.dump(matrix, outfile_matrix)
    # with open('./static/distance_matrix.json') as matrix_file:
    #     matrix = json.load(matrix_file)
    dist = Clr.get_distance_matrix_values(matrix)
    votes = gph.calculate_graph(dist, markers, matrix)
    svg_f.generate_svg(votes)
    return redirect(url_for('draw_svg'))


@app.route('/graph', methods=['GET', 'POST'])
def draw_svg():
    form = Form()
    svg = None
    if form.validate_on_submit():
        num = form.number.data
        graph = gph.connected_graph(num)
        svg_f.generate_svg(graph)
        return redirect(url_for('draw_svg'))
    elif request.method == 'GET':
        form.max_votes = session['max_votes']
        form.min_votes = session['min_votes']
        svg = render_template('./grafo_svg.svg')
    return render_template('show_graph.html', form=form, svg=svg)


# @app.route("/saveNumber", methods=['POST', 'GET'])
# def save_number():
#     num = int(request.get_data())
#     graph = gph.connected_graph(num)
#     svg_f.generate_svg(graph)
#     return redirect(url_for('draw_svg'))

# @app.route('/setMode', methods=['POST'])
# def set_mode():
#     mode_form = ModeForm()
#     if mode_form.validate_on_submit():
#         num = mode_form.number.data
#         mode = mode_form.mode.data
#     return render_template('map_template.html', form=mode_form)


@app.route('/setMode', methods=['POST'])
def set_mode():
    mode = request.form['mode']
    session['mode'] = mode
    if mode:
        return jsonify('OK')
    return jsonify('ERROR')


@app.route('/api/mensaje')
def mensaje():
    return render_template('vue_template.html')

