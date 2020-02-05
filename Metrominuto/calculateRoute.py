from random import sample

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
    # print(distances)
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
    vote_graph = nx.Graph()
    nodes_name = 0
    for node in nodes:
        graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        min_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        vote_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        nodes_name = nodes_name + 1

    for i in range(0, dista.__len__()):
        for j in range(0, dista.__len__()):
            if i != j:
                graph.add_edge(str(i), str(j), weight=dista[i][j])
    # mst = nx.minimum_spanning_tree(graph, weight='weight')
    # nx.draw(mst, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True)

    # mst = nx.minimum_spanning_edges(graph, weight='weight', data=True)
    # edge_list = list(mst)  # make a list of the edges
    # prueba = sample(edge_list, k=2)
    # for z in range(0, edge_list.__len__()):
    #     min_graph.add_edge(edge_list[z][0], edge_list[z][1], weight=edge_list[z][2]['weight'])
    # nx.draw(min_graph, pos=nx.get_node_attributes(graph, 'pos'), with_labels=True)
    #
    # plt.show()
    save_nodes_json(graph)
    # votes = nodes_votes(graph, nodes_name, min_graph, vote_graph)
    # print(votes)
    # draw_line = 23
    # elarge = [(u, v) for (u, v, d) in votes.edges(data=True) if d['votes'] > 15]
    # # positions for all nodes
    # pos = nx.spring_layout(votes)
    # # nodes
    # nx.draw_networkx_nodes(votes, pos, node_size=700)
    # # edges
    # nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6)
    # nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6, alpha=0.5, edge_color='b', style='dashed')
    # # labels
    # nx.draw_networkx_labels(votes, pos, font_size=20, font_family='sans-serif')
    # plt.axis('off')
    # plt.show()
    return 0


def save_nodes_json(graph):
    # data = {'stations': {}, 'lines': []}
    stat = {'stations': {}, 'lines': []}
    # Generar estaciones
    for node in graph.nodes(data=True):
        stat['lines'].append({'name': node[0],
                              'shiftCoords'[0]: node[1]['pos'][0], 'shiftCoords'[1]: node[1]['pos'][1],
                              'nodes': []})

    for node in graph.nodes(data=True):
        stat['stations'][node[0]] = {}
        stat['stations'][node[0]]['name'] = node[0]
        stat['stations'][node[0]]['position'] = {}
        stat['stations'][node[0]]['position']['lat'] = node[1]['pos'][0]
        stat['stations'][node[0]]['position']['lng'] = node[1]['pos'][1]



    print(stat)
    return 0


def nodes_votes(graph, tam, min_graph, votes_graph):
    votes = np.zeros((tam, tam))
    edge_list = list(graph.edges(data=True))  # make a list of the edges
    votes_graph.clear()
    # Bucle para sacar los votos aleatorios del grafo
    for i in range(0, 100):
        random_graph = sample(edge_list, k=tam - 1)
        min_graph.clear()
        for z in range(0, random_graph.__len__()):
            min_graph.add_edge(random_graph[z][0], random_graph[z][1], weight=random_graph[z][2]['weight'])
        mst = nx.minimum_spanning_edges(min_graph, weight='weight', data=True)
        edge_list_min = list(mst)  # make a list of the edges
        for pair in edge_list_min:
            x = int(pair[0])
            y = int(pair[1])
            votes[x, y] = votes[x, y] + 1
            votes_graph.add_edge(random_graph[z][0], random_graph[z][1], votes=votes[x, y] + 1)
    return votes_graph


def ejemplo_graph():
    G = nx.Graph()

    G.add_edge('a', 'b', weight=0.6)
    G.add_edge('a', 'c', weight=0.2)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]
    pos = nx.spring_layout(G)  # positions for all nodes
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=700)
    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=6, alpha=0.5, edge_color='b', style='dashed')
    # labels
    nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')
    plt.axis('off')
    plt.show()
    return 0