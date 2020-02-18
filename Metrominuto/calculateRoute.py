from random import sample
import networkx as nx
import json
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


def calculate_graph(dista, nodes):
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
    votes, max, min = nodes_votes(graph, nodes_name, min_graph, vote_graph)
    draw_value = (max + min)/2
    draw_votes_graph(votes, draw_value)
    save_nodes_json(votes, graph)
    return 0


def save_nodes_json(min_graph, weight_graph):
    stations = {}
    pos = weight_graph.nodes(data=True)
    for node in min_graph.nodes(data=True):
        stations[node[0]] = {}
        stations[node[0]]['label'] = node[0]
        stations[node[0]]['position'] = {}
        stations[node[0]]['position']['lat'] = pos._nodes[node[0]]['pos'][0]
        stations[node[0]]['position']['lng'] = pos._nodes[node[0]]['pos'][1]

    nodes_dict_min = dict(min_graph.nodes(data=True))  # make a dict of the nodes
    edge_list_min = list(min_graph.edges(data=True))  # make a list of the edges
    # print(nodes_dict_min)
    # print(edge_list_min)
    #line 1
    lines_list = [{'name': 'Line1', 'label': 'Line1', 'color': '#FFD600', 'shiftCoords': [0, 0], 'nodes': []}]
    for edge in edge_list_min:
        lines_list[0]['nodes'].append({'name': edge[0],
                                       'coords': [pos._nodes[edge[0]]['pos'][0]*10000,pos._nodes[edge[0]]['pos'][1]*10000],
                                       'labelPos': 'S',
                                       'marker': 'interchange'})
        lines_list[0]['nodes'].append({'coords':[pos._nodes[edge[1]]['pos'][0]*10000,pos._nodes[edge[0]]['pos'][1]*10000]})
        lines_list[0]['nodes'].append({'name': edge[1],
                                       'coords': [pos._nodes[edge[1]]['pos'][0]*10000, pos._nodes[edge[1]]['pos'][1]*10000],
                                       'labelPos': 'S',
                                       'marker': 'interchange'})
    data = {'stations': stations, 'lines': lines_list}
    with open('./static/result.json', 'w') as fp:
        json.dump(data, fp)
    print(data)
    return 0


def nodes_votes(graph, tam, min_graph, votes_graph):
    votes = np.zeros((tam, tam))
    edge_list = list(graph.edges(data=True))  # make a list of the edges
    votes_graph.clear()
    # Bucle para sacar los votos aleatorios del grafo
    for i in range(0, 50):
        random_graph = sample(edge_list, k=tam-2)
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
    return votes_graph, np.max(votes), np.min(votes)


def draw_votes_graph(votes, draw_line):
    elarge = [(u, v) for (u, v, d) in votes.edges(data=True) if d['votes'] > draw_line]
    # positions for all nodes
    pos = nx.spring_layout(votes)
    # nodes
    nx.draw_networkx_nodes(votes, pos, node_size=600, label=votes.nodes)
    # edges
    nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6)
    # labels
    nx.draw_networkx_labels(votes, pos, font_size=20, font_family='sans-serif')
    plt.axis('auto')
    plt.show()
    return 0

