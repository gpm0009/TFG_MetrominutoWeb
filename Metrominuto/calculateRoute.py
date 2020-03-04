from random import sample
import networkx as nx
import json
import numpy as np
import matplotlib.pyplot as plt
import svgwrite as svg
from sys import stdout


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
    weight = nx.get_edge_attributes(graph, 'weight')
    votes = nodes_votes(graph, nodes_name, min_graph, vote_graph, weight)
    draw_votes_graph(votes)
    # save_svg()
    generate_svg(votes)
    return 0


def nodes_votes(graph, tam, min_graph, votes_graph, weight):
    votes = np.zeros((tam, tam))
    edge_list = list(graph.edges(data=True))  # make a list of the edges
    # votes_graph.clear()
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
            votes_graph.add_edge(random_graph[z][0], random_graph[z][1],
                                 weight=weight[(random_graph[z][0], random_graph[z][1])],
                                 votes=votes[x, y] + 1)
    return votes_graph


def draw_votes_graph(votes):
    # nodes
    # nx.draw_networkx_nodes(votes, pos, label=votes.nodes, node_color='#80b41f')
    # # edges
    # nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6)
    # # labels
    # nx.draw_networkx_labels(votes, pos, font_size=20, font_family='sans-serif')
    plt.figure(figsize=[10, 10])
    plt.axis('off')
    nx.draw_networkx(votes, pos=nx.get_node_attributes(votes, 'pos'), node_color='#80b41f')
    plt.show()
    return 0


#posterior a que el usuario elija un parámetro.
def conected_graph(graph_pos, graph_votes, position):
    connected_components = sorted(nx.connected_components(graph_votes), key=len, reverse=True)
    print(connected_components)
    # if the graph is not connected
    if connected_components.__len__() == 1:
        edge_list = list(graph_votes.edges(data=True))
        graph_connected = nx.Graph()
        for node in graph_pos.nodes(data=True):
            graph_connected.add_node(node[0], pos=(node[1]['pos'][0], node[1]['pos'][1]))

        for component in connected_components:
            print(component)

    return 0


def save_svg():
    dwg = svg.Drawing('templates/test.svg', size=("800px", "600px"), profile='full')
    line = dwg.line(id='line1',start=(295, 50), end=(95, 75), stroke='#000', stroke_width=5)
    dwg.add(line)
    line = dwg.line(id='line2', start=(400, 50), end=(300, 30), stroke='#000', stroke_width=5)
    dwg.add(line)
    dwg.save(pretty=True)
    return 0


def generate_svg(graph_votes):
    dwg = svg.Drawing('templates/grafo_svg.svg', size=('900px', '900px'),viewBox=('-100 -100 200 200'), profile='full')
    for node in (graph_votes.nodes(data=True)):
        circle = dwg.circle(id='node'+node[0], center=(node[1]['pos'][0], node[1]['pos'][1]), r='3')
        dwg.add(circle)

    positions = nx.get_node_attributes(graph_votes, 'pos')
    for edge in (graph_votes.edges(data=True)):
        line = dwg.line(id='line'+str(int(edge[2]['votes'])),
                        start=(positions[edge[0]][0], positions[edge[0]][1]),
                        end=(positions[edge[1]][0], positions[edge[1]][1]),
                        stroke='#000', stroke_width=1)
        dwg.add(line)
    dwg.save(pretty=True)
    return 0