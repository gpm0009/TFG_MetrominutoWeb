import networkx as nx
from flask import Flask, render_template, request, jsonify, json
from datetime import datetime
import googlemaps
import numpy as np
import matplotlib.pyplot as plt

# recibe un diccionario
def read_matrix_distance(matrix_distance):
    rows = matrix_distance['rows']  # Lista de disccionarios.
    # matrix['rows'][0]['elements'][0]['distance']['value']
    for row in rows:
        elements = row['elements']
        for element in elements:
            distance = element['distance']['value']
    # matrix['destination_addresses'][0]
    destination_addresses = matrix_distance['destination_addresses']  # List
    origin_addresses = matrix_distance['origin_addresses']  # List
    get_distance_matrix_values(matrix_distance)
    return 0


def get_distance_matrix_values(matrix_distance):
    x = matrix_distance['origin_addresses'].__len__()
    y = matrix_distance['destination_addresses'].__len__()
    distances = np.zeros((x, y))
    for i in range(0, x):
        for j in range(0, y):
            distances[i, j] = matrix_distance['rows'][i]['elements'][j]['distance']['value']
    print(distances)
    return distances


# recibe una lista con un diccionario.
def read_direction(directions):
    trace = directions[0]  # Diccionario
    # directions_result[0]['warnings'][0]
    # directions_result[0]['waypoint_order']
    # directions_result[0]['legs'][0]['distance']['value']
    # directions_result[0]['legs'][0]['end_location']['lat']
    warnings = trace['warnings']
    for warnin in warnings:
        print(warnin)
    legs = trace['legs']
    return 0


def draw_graph(dista, nodes):
    graph = nx.Graph()
    min_graph = nx.Graph()
    nodes_name = 0
    for node in nodes:
        graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        min_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        nodes_name = nodes_name + 1

    for i in range(0, dista.__len__()):
        for j in range(0, dista.__len__()):
            if i != j:
                graph.add_edge(str(i), str(j), weight=dista[i][j])
    # nx.draw(graph, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True)
    mst = nx.minimum_spanning_edges(graph, weight='weight', data=True)

    edgelist = list(mst)  # make a list of the edges
    print(sorted(edgelist))

    for z in range(0, edgelist.__len__()):
        min_graph.add_edge(edgelist[z][0], edgelist[z][1], weight=edgelist[z][2]['weight'])
    nx.draw(min_graph, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True)
    # nx.draw_networkx_edge_labels(graph, pos=nx.get_node_attributes(graph, 'pos'), edge_labels=None, label_pos=0.5,
    #                         font_size=10, font_color='k',
    #                         font_family='sans-serif', font_weight='normal', alpha=None, bbox=None, ax=None,
    #                         rotate=True)
    plt.show()
    return 0
