"""
    metrominuto_app.main.routes
    This file contains the routes of the main module.
"""
import json
from datetime import datetime

import googlemaps
from flask import redirect, url_for, render_template, request, session

from config import Config
from metrominuto_app import globals
from metrominuto_app import svgfunctions as svg_f, graphs as gph, calculateRoute as Clr
from metrominuto_app.main import main
from metrominuto_app.main.forms import MapForm, Form, LogInForm
from metrominuto_app.utils.decorators import log_in

google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)


@main.route("/", methods=['GET', 'POST'])
def index():
    form = LogInForm()
    if request.method == 'POST':
        user_info = json.loads(request.form['user_data'])
        session['email'] = user_info['data']['email']
        return redirect(url_for('main.set_marks'))
    return render_template('index.html', form=form)


@main.route("/widget", methods=['GET', 'POST'])
def widget():
    return render_template('widget.html')


@main.route("/logut", methods=['GET', 'POST'])
def logout():
    session.clear()
    if request.method == 'POST':
        return redirect(url_for('main.index'))


@main.route("/map", methods=['GET', 'POST'])
@log_in
def set_marks():
    # with open('metrominuto_app/static/distance_matrix_example2.json') as matrix_file:
    #     matrix = json.load(matrix_file)
    # with open('metrominuto_app/static/markers_example2.json') as markers_file:
    #     new_markers = json.load(markers_file)
    # new_markers = new_markers['markers']
    markers = []
    # for element in new_markers:
    #     markers.append(element)
    origins = []
    destinations = []
    text_size = {}
    text_size_id = []
    form = MapForm()
    if request.method == 'POST':
        mode = form.mode.data
        size = json.loads(request.form['size'])
        for width in size['size']:
            text_size[width['id']] = {'size': width['size'], 'text': width['text']}
            text_size_id.append(width['id'])
        globals.global_widths = text_size
        request_markers = json.loads(request.form['markers'])
        for mark in request_markers['markers']:
            markers.append(mark)
            origins.append(mark['position'])
            destinations.append(mark['position'])
        central_markers = json.loads(request.form['central_markers'])
        now = datetime.now()
        matrix = google_maps.distance_matrix(origins, destinations, 'walking', departure_time=now)
        # with open('metrominuto_app/static/distance_matrix_example2.json') as matrix_file:
        #     matrix = json.load(matrix_file)
        globals.global_dirs = text_size
        dist = Clr.get_distance_matrix_values(matrix, text_size_id)
        gph.calculate_graph(dist, markers, central_markers['central_markers'], matrix)
        session['marcadores'] = json.dumps(markers)
        session['grafo'] = 1
        return redirect(url_for('main.draw_svg'))
    longitude = -3.69
    latitude = 42.34
    return render_template(
        'map_template.html',
        longitude=longitude,
        latitude=latitude, API_KEY=Config.GOOGLE_API_KEY, form=form)  #, matrix=json.dumps(matrix['destination_addresses']))  # positions=json.dumps(markers)


@main.route('/graph', methods=['GET', 'POST'])
@log_in
def draw_svg():
    form = Form()
    if request.method == 'POST':
        session['id_svg_selected'] = int(request.form['formControlRange'])
        return redirect(url_for('main.edit_graph'))
    svg_list = []
    svg_dict = {}
    cont_colors_dict = {}
    for i in range(0, int(session['max_votes'])):  # 1):  #int(session['max_votes'])):  # 1):
        graph = gph.connected_graph(i)
        svg, graph_class, cont_color = svg_f.draw_metrominuto(graph)
        svg_list.append(svg)
        svg_dict[str(i)] = graph_class.__dict__
        cont_colors_dict[str(i)] = {'green': cont_color.num_green,
                                    'red': cont_color.num_red,
                                    'blue': cont_color.num_blue,
                                    'purple': cont_color.num_purple,
                                    'brown': cont_color.num_brown}
    session['svg_graphs_dict'] = svg_dict
    session['svg_cont_colors'] = cont_colors_dict
    return render_template('show_graph.html', max=session['max_votes'] - 1, min=session['min_votes'], lista=svg_list, form=form, cont_colors_dict=cont_colors_dict)


@main.route('/graph/edit', methods=['GET', 'POST'])
@log_in
def edit_graph():
    cont_colors = session['svg_cont_colors'][str(session['id_svg_selected'])]
    return render_template('edit_graph.html', grafo=session['svg_graphs_dict'][str(session['id_svg_selected'])], cont_colors=cont_colors)


@main.route('/recalcule', methods=['POST'])
def recalcule():
    grafo = json.loads(request.data)
    g = svg_f.recalcule_positions(grafo)
    return g.__dict__


@main.route('/ayuda')
def help_page():
    return render_template('ayuda.html')
