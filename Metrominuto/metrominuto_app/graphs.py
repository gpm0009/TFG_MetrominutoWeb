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
    graph = nx.Graph()
    min_graph = nx.Graph()
    nodes_name = 0
    for node in nodes:
        graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']), id=node['id'])
        min_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']), id=node['id'])
        globals.vote_global_graph.add_node(str(nodes_name),
                                           pos=(node['position']['lat'], node['position']['lng']),
                                           id=node['id'])
        nodes_name = nodes_name + 1

    for i in range(0, distances.__len__()):
        for j in range(0, distances.__len__()):
            if i != j:
                graph.add_edge(str(i), str(j), weight=distances[i][j],
                               duration=matrix['rows'][i]['elements'][j]['duration']['text'])
    # votes = nodes_votes(graph, nodes_name, min_graph)
    votes = calculate_edges_votes(graph, nodes_name, central_markers)
    return votes


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
        central_markers_id.append(central_mark['id'])
    votes = np.zeros((tam, tam))
    graph_nodes = list(graph.nodes(data='id'))
    for i in range(1, tam):
        if graph_nodes[i][1] not in central_markers_id:
            random_graph = copy.deepcopy(graph)
            # print('OUT')
            random_graph.remove_node(str(i))
            mst = nx.minimum_spanning_edges(random_graph, weight='weight', data=True)
            edge_list_min = list(mst)  # make a list of the minimum edges
            for pair in edge_list_min:
                x = int(pair[0])
                y = int(pair[1])
                votes[x, y] = votes[x, y] + 1
                globals.vote_global_graph.add_edge(pair[0], pair[1],
                                                   weight=pair[2]['weight'],
                                                   votes=votes[x, y], duration=pair[2]['duration'])
    session['max_votes'] = votes.max()
    session['min_votes'] = votes.min()
    return globals.vote_global_graph


# old
def nodes_votes(graph, tam, min_graph):
    weight = nx.get_edge_attributes(graph, 'weight')
    votes = np.zeros((tam, tam))
    edge_list = list(graph.edges(data=True))  # make a list of the edges
    # votes_graph.clear()
    # Bucle para sacar los votos aleatorios del grafo
    for i in range(0, 50):
        random_graph = sample(edge_list, k=tam - 2)
        min_graph.clear()
        for z in range(0, random_graph.__len__()):
            min_graph.add_edge(random_graph[z][0], random_graph[z][1], weight=random_graph[z][2]['weight'])
        mst = nx.minimum_spanning_edges(min_graph, weight='weight', data=True)
        edge_list_min = list(mst)  # make a list of the edges
        for pair in edge_list_min:
            x = int(pair[0])
            y = int(pair[1])
            votes[x, y] = votes[x, y] + 1
            globals.vote_global_graph.add_edge(random_graph[z][0], random_graph[z][1],
                                               weight=weight[(random_graph[z][0], random_graph[z][1])],
                                               votes=votes[x, y] + 1, duration=random_graph[z][2]['duration'])
    # print(votes)
    session['max_votes'] = votes.max()
    session['min_votes'] = votes.min()
    return globals.vote_global_graph


def draw_votes_graph():
    # nodes
    # nx.draw_networkx_nodes(votes, pos, label=votes.nodes, node_color='#80b41f')
    # # edges
    # nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6)
    # # labels
    # nx.draw_networkx_labels(votes, pos, font_size=20, font_family='sans-serif')
    plt.figure(figsize=[10, 10])
    plt.axis('off')
    nx.draw_networkx(globals.vote_global_graph, pos=nx.get_node_attributes(globals.vote_global_graph, 'pos'),
                     node_color='#80b41f')
    plt.show()
    return 0


def draw_graph(grafo):
    plt.figure(figsize=[10, 10])
    plt.axis('off')
    nx.draw_networkx(grafo, pos=nx.get_node_attributes(grafo, 'pos'), node_color='#80b41f')
    plt.show()
    return 0


# posterior a que el usuario elija un parámetro.
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
                time = 'default'
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
            if globals.global_matrix[element_x, element_y] < min:
                min = globals.global_matrix[element_x, element_y]
                nodex = element_x
                nodey = element_y
    return nodex, nodey, min
