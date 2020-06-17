"""
    metrominuto_app.graphs

    This file contains NetworkX operations with graphs in order to calculate
    votes and the final graph.
"""
from random import sample
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from flask import session
import copy
from metrominuto_app import globals


def calculate_positions(nodes):
    """Funcion that calculate new position bases in Ln scale.
    :param nodes: Points or markers selected in the map.
    :type: dict.
    :return: node positions.
    :rtype: list.
    """
    coords_x = []
    coords_y = []
    for node in nodes:
        coords_x.append(node['position']['lng'])
        coords_y.append(node['position']['lat'])
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    dif_x = (max_x - min_x)
    dif_y = (max_y - min_y)
    node_positions = []
    x_normalize = []
    y_normalize = []
    for node in nodes:
        pos_x = (node['position']['lng'] - min_x) / dif_x
        pos_y = 1.4 - (node['position']['lat'] - min_y) / dif_y
        if pos_x == 0.0:
            pos_x = -1.0
        else:
            pos_x = np.log10(pos_x)
        x_normalize.append(pos_x)
        if pos_y == 0.0:
            pos_y = -1.0
        else:
            pos_y = np.log10(pos_y)
            y_normalize.append(pos_y)
        node_positions.append([pos_x, pos_y])
    max_x_normalize, min_x_normalize = max(x_normalize), min(x_normalize)
    max_y_normalize, min_y_normalize = max(y_normalize), min(y_normalize)
    dif_x_normalize = (max_x_normalize - min_x_normalize)
    dif_y_normalize = (max_y_normalize - min_y_normalize)
    return_positions = []
    for pos in node_positions:
        x = (pos[0] - min_x_normalize) / dif_x_normalize
        y = (pos[1] - min_y_normalize) / dif_y_normalize
        return_positions.append([x, y])
    return return_positions


def calculate_graph(distances, nodes, central_markers, matrix):
    """
    
    :param distances: Array with distances between all points.
    :type distances: Array

    :param nodes: One or more locations with latitude/longitude and id values
    :type nodes: list

    :param central_markers: One or more locations with latitude/longitude and id values
        that indicates which points are going to be centrals. It means those points are
        going to be always in the minimum spanning tree.
    :type central_markers: list

    :param matrix: Travel distances and times for a matrix of origins and destinations
    :type matrix: dict

    :return: votes: NetworkX graph that contains all nodes with position and id as attributes, and
        edges with distance, duration and votes as attributes.
    :rtype: NetworkX graph
    """
    coords_x = []
    coords_y = []
    for node in nodes:
        if node['position']['lng'] < 0:
            coords_x.append(-np.log10(abs(node['position']['lng'])))
        else:
            coords_x.append(np.log10(node['position']['lng']))
        if node['position']['lat'] < 0:
            coords_y.append(-np.log10(abs(node['position']['lat'])))
        else:
            coords_y.append(np.log10(node['position']['lat']))
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    dif_x = (max_x - min_x)
    dif_y = (max_y - min_y)

    graph = nx.Graph()
    min_graph = nx.Graph()
    nodes_name = 0
    # new_positions = calculate_positions(nodes)
    calculate_rejilla = []
    for index, node in enumerate(nodes):
        pos_x = (coords_x[index] - min_x) / dif_x
        pos_y = 1.4 - (coords_y[index] - min_y) / dif_y
        calculate_rejilla.append([pos_x, pos_y])
    positions = rejilla(calculate_rejilla)
    globals.vote_global_graph.clear()
    for index, node in enumerate(nodes):
        pos_x = positions[index][0]
        pos_y = positions[index][1]
        min_graph.add_node(str(node['id']), pos=(pos_x, pos_y), id=node['id'])
        globals.vote_global_graph.add_node(str(node['id']),
                                           pos=(pos_x, pos_y),
                                           id=node['id'])
        print('Node Aded -> ', node['id'], ' + ', str(node['id']))
        nodes_name = nodes_name + 1

    for i, node in enumerate(nodes):
        for j, node_aux in enumerate(nodes):
            if i != j:
                graph.add_edge(str(node['id']), str(node_aux['id']), weight=distances[i][j],
                               duration=matrix['rows'][i]['elements'][j]['duration']['text'])

    # for i in range(0, distances.__len__()):
    #     for j in range(0, distances.__len__()):
    #         if i != j:
    #             graph.add_edge(str(i), str(j), weight=distances[i][j],
    #                            duration=matrix['rows'][i]['elements'][j]['duration']['text'])
    votes = calculate_edges_votes(graph, nodes_name, central_markers)
    return votes


def rejilla(positions):
    """Function that recalculates the positions of the nodes in order to establish a grid and align said nodes.

    :param positions: list of nodes positions in order to be replace.
    :type positions: list

    :return positions: List of nodes with new position.
    :rtype positions: list
    """
    max_x, min_x = max(positions[:][0]), min(positions[:][0])
    max_y, min_y = max(positions[:][1]), min(positions[:][1])
    for tramo_x in np.arange(min_x, max_x, 0.07):
        for i in range(0, positions.__len__()):
            if tramo_x <= positions[i][0] <= (tramo_x+0.07):
                positions[i][0] = (tramo_x + tramo_x+0.07) / 2

    for tramo_y in np.arange(min_y, max_y, 0.07):
        for j in range(0, positions.__len__()):
            if tramo_y <= positions[j][1] <= tramo_y+0.07:
                positions[j][1] = (tramo_y + tramo_y+0.07) / 2

    return positions


def calculate_edges_votes(graph, tam, central_markers):
    """Functions that calculates edges votes and make corresponding graph.

    :param graph: NetworkX graph that contains all nodes and edges with positions, distance and duration.
    :type graph: NetworkX graph

    :param tam: Number that indicates the total number of elements and the names of the nodes
    :type tam: Integer

    :param central_markers: One or more locations with latitude/longitude and id values
        that indicates which points are going to be centrals. It means those points are
        going to be always in the minimum spanning tree.
    :type central_markers: list

    :return: globals.vote_global_graph: global variable containing graph with all nodes and edges
        with duration, distance and votes as attributes.
    :rtype: NetworkX graph
    """
    central_markers_id = []
    for central_mark in central_markers:
        central_markers_id.append(str(central_mark['id']))

    votes_aux = {}
    graph_nodes = list(graph.nodes(data='id'))
    l_max = []
    for node in graph_nodes:
        l_max.append(int(node[0]))
    tam_aux = max(l_max)+1
    votes = np.zeros((tam_aux, tam_aux))
    for i in graph_nodes:
        if i[0] not in central_markers_id:
            random_graph = copy.deepcopy(graph)
            # print('OUT')
            random_graph.remove_node(i[0])
            mst = nx.minimum_spanning_edges(random_graph, weight='weight', data=True)
            edge_list_min = list(mst)  # make a list of the minimum edges
            for pair in edge_list_min:
                x = int(pair[0])
                y = int(pair[1])
                votes[x, y] = votes[x, y] + 1
                globals.vote_global_graph.add_edge(pair[0], pair[1],
                                                   weight=pair[2]['weight'],
                                                   votes=votes[x, y], duration=pair[2]['duration'])
                print('Edge Added-> ', pair[0], ' - ', pair[1])
    session['max_votes'] = votes.max()
    session['min_votes'] = votes.min()
    return globals.vote_global_graph


def connected_graph(num_votes):
    """Function that receives a number and check if the global.votes_graph are connected.

    :param num_votes: Number that indicates the number of votes that all edged have to have.
    :type num_votes: Integer.

    :return check_graph: fully connected graph whose arcs have the votes indicated by number_votes.
    :rtype: NetworkX graph.
    """
    check_graph = nx.Graph()
    for node in (globals.vote_global_graph.nodes(data=True)):
        check_graph.add_node(node[0], pos=node[1]['pos'])
    for edge in (globals.vote_global_graph.edges(data=True)):
        if int(edge[2]['votes']) > num_votes:
            check_graph.add_edge(edge[0], edge[1], weight=edge[2]['weight'], votes=edge[2]['votes'],
                                 duration=edge[2]['duration'])
    connected_components_list = sorted(nx.connected_components(check_graph), key=len, reverse=True)
    # print(connected_components_list)
    # if the graph is not connected
    if connected_components_list.__len__() > 1:
        for s in range(0, connected_components_list.__len__() - 1):
            node_x, node_y, dist = compare_distance_matrix(connected_components_list[0], connected_components_list[1])
            edge_duration = globals.vote_global_graph.get_edge_data(str(node_x), str(node_y))
            if edge_duration is not None:
                time = edge_duration['duration']
            else:
                time = globals.global_durations[node_x][node_y]
            check_graph.add_edge(str(node_x), str(node_y), weight=dist, duration=time)
            # draw_graph(check_graph)
            connected_components_list = sorted(nx.connected_components(check_graph), key=len, reverse=True)
            # print(connected_components_list)
    return check_graph


def compare_distance_matrix(component_x, component_y):
    """
    Function that calculates what node that is closest.

    :param component_x:
    :type: set

    :param component_y:
    :type: set

    :return: nodex, nodey: Point coordinates of the node that is closest
    :rtype: int

    :return: min: Minimum distance between the points.
    :rtype: float
    """
    min = 9999999
    for x in range(0, component_x.__len__()):
        element_x = int(component_x.pop())
        for y in range(0, component_y.__len__()):
            element_y = int(component_y.pop())
            if globals.global_matrix[str(element_x)][str(element_y)] < min:
                min = globals.global_matrix[str(element_x)][str(element_y)]
                nodex = element_x
                nodey = element_y
    return nodex, nodey, min
