"""
    metrominuto_app.main.routes

    This file contains the routes of the main module.
"""
import json
from datetime import datetime
from pprint import pprint

import networkx as nx

from metrominuto_app import svgfunctions as svg_f, graphs as gph, calculateRoute as Clr
from flask import render_template, request, session, jsonify, redirect, url_for
from config import Config
from metrominuto_app.main.forms import MapForm, Form
import googlemaps
from metrominuto_app.main import main
import os

google_maps = googlemaps.Client(key=Config.GOOGLE_API_KEY)


@main.route("/", methods=['GET', 'POST'])
def set_marks():
    with open('metrominuto_app/static/markers_example2.json') as markers_file:
        new_markers = json.load(markers_file)
    new_markers = new_markers['markers']
    markers = []
    for element in new_markers:
        markers.append(element)
    origins = []
    destinations = []
    form = MapForm()
    if request.method == 'POST':
        mode = form.mode.data
        request_markers = json.loads(request.form['markers'])
        # for mark in request_markers['markers']:
        #     markers.append(mark)
        #     origins.append(mark['position'])
        #     destinations.append(mark['position'])
        central_markers = json.loads(request.form['central_markers'])
        # now = datetime.now()
        # matrix = google_maps.distance_matrix(origins, destinations, 'walking', departure_time=now)
        with open('metrominuto_app/static/distance_matrix_example2.json') as matrix_file:
            matrix = json.load(matrix_file)
        dist = Clr.get_distance_matrix_values(matrix)
        gph.calculate_graph(dist, markers, central_markers['central_markers'], matrix)
        session['marcadores'] = json.dumps(markers)
        session['grafo'] = 1
        return redirect(url_for('main.draw_svg'))
    longitude = -3.69
    latitude = 42.34
    return render_template(
        'map_template.html',
        longitude=longitude,
        latitude=latitude, API_KEY=Config.GOOGLE_API_KEY, form=form,
        positions=json.dumps(markers))  # positions=json.dumps(markers)


@main.route('/graph', methods=['GET', 'POST'])
def draw_svg():
    form = Form()
    if request.method == 'POST':
        session['id_svg_selected'] = int(request.form['formControlRange'])
        return redirect(url_for('main.edit_graph'))
    svg_list = []
    svg_dict = {}
    for i in range(0, int(session['max_votes'])):  # 1):  #int(session['max_votes'])):  # 1):
        graph = gph.connected_graph(i)
        svg, positions_list = svg_f.draw_metrominuto(graph)
        svg_list.append(svg)
        svg_dict[str(i)] = svg_f.Graphs(graph.nodes(data=True), graph.edges(data=True), positions_list['node'], positions_list['edges']).__dict__
    session['svg_list_sent'] = svg_list
    session['svg_graphs_dict'] = svg_dict
    return render_template('show_graph.html', max=session['max_votes'] - 1, min=session['min_votes'], lista=svg_list, form=form)


@main.route('/graph/edit', methods=['GET', 'POST'])
def edit_graph():
    svg = session['svg_list_sent'][session['id_svg_selected']]
    return render_template('edit_graph.html', svg=svg)


@main.route('/setMode', methods=['POST'])
def set_mode():
    mode = request.form['mode']
    session['mode'] = mode
    if mode:
        return jsonify('OK')
    return jsonify('ERROR')


@main.route('/prueba')
def mensaje():
    # with open('metrominuto_app/static/prueba_grafo.json') as markers_file:
    #     new_markers = json.load(markers_file)
    # with open('metrominuto_app/static/prueba_positions.json') as post:
    #     positions = json.load(post)
    # return render_template('template.html', grafo=session['svg_graphs_dict'][str(session['id_svg_selected'])])
    return render_template('template.html', grafo=session['svg_graphs_dict']['0'])


@main.route('/modal')
def prueba():
    return render_template('vue_template.html')


@main.route('/ayuda')
def help_page():
    return render_template('ayuda.html')
