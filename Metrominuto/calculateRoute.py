from random import sample
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import svgwrite as svg
import globals


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
    globals.global_matrix = distances
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


# global graph with all attributes (position, weight, votes).
vote_global_graph = nx.Graph()


def calculate_graph(dista, nodes):
    graph = nx.Graph()
    min_graph = nx.Graph()
    # vote_graph = nx.Graph()
    nodes_name = 0

    for node in nodes:
        graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        min_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        vote_global_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        nodes_name = nodes_name + 1

    for i in range(0, dista.__len__()):
        for j in range(0, dista.__len__()):
            if i != j:
                graph.add_edge(str(i), str(j), weight=dista[i][j])
    weight = nx.get_edge_attributes(graph, 'weight')
    votes = nodes_votes(graph, nodes_name, min_graph, weight)
    # draw_votes_graph(votes)
    # save_svg()
    generate_svg(votes)
    return 0


def nodes_votes(graph, tam, min_graph, weight):
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
            vote_global_graph.add_edge(random_graph[z][0], random_graph[z][1],
                                       weight=weight[(random_graph[z][0], random_graph[z][1])],
                                       votes=votes[x, y] + 1)
    print(votes)
    return vote_global_graph


def draw_votes_graph(votes):
    # nodes
    # nx.draw_networkx_nodes(votes, pos, label=votes.nodes, node_color='#80b41f')
    # # edges
    # nx.draw_networkx_edges(votes, pos, edgelist=elarge, width=6)
    # # labels
    # nx.draw_networkx_labels(votes, pos, font_size=20, font_family='sans-serif')
    plt.figure(figsize=[10, 10])
    plt.axis('off')
    nx.draw_networkx(vote_global_graph, pos=nx.get_node_attributes(vote_global_graph, 'pos'), node_color='#80b41f')
    plt.show()
    return 0


def draw_graph(grafo):
    plt.figure(figsize=[10, 10])
    plt.axis('off')
    nx.draw_networkx(grafo, pos=nx.get_node_attributes(grafo, 'pos'), node_color='#80b41f')
    plt.show()
    return 0


def save_svg():
    dwg = svg.Drawing('templates/test.svg', size=("800px", "600px"), profile='full')
    line = dwg.line(id='line1', start=(295, 50), end=(95, 75), stroke='#000', stroke_width=5)
    dwg.add(line)
    line = dwg.line(id='line2', start=(400, 50), end=(300, 30), stroke='#000', stroke_width=5)
    dwg.add(line)
    dwg.save(pretty=True)
    return 0


def generate_svg(graph_votes):
    pos = nx.get_node_attributes(graph_votes, 'pos')
    coords_x = []
    coords_y = []
    for x in range(0, pos.__len__()):
        coords_x.append(pos[str(x)][0])
        coords_y.append(pos[str(x)][1])
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    # print(max_x, ' | ', min_x, ' | ', max_y, ' | ', min_y)
    radio = 0.06
    vB = '-'+str(min_x-radio) + ' '+ str(min_y-radio) + ' ' + str(max_x-min_x) + ' ' + str(max_y-min_y)

    print(min_x, ' | ', max_x)
    print(max_x-min_x)
    file_name = 'templates/grafo_svg.svg'
    dwg = svg.Drawing(file_name, size=('900px', '900px'),
                      viewBox='-1 -1 3 3', profile='full')
    for node in (graph_votes.nodes(data=True)):
        coox = (node[1]['pos'][0] - min_x)/(max_x - min_x)
        cooy = (node[1]['pos'][1] - min_y)/(max_y - min_y)
        circle = dwg.circle(id='node' + node[0], center=(coox, cooy), r=str(radio))
        dwg.add(circle)
    positions = nx.get_node_attributes(graph_votes, 'pos')
    for edge in (graph_votes.edges(data=True)):
        line = dwg.line(id='line',
                        start=((positions[edge[0]][0]- min_x)/(max_x - min_x), (positions[edge[0]][1]- min_y)/(max_y - min_y)),
                        end=((positions[edge[1]][0]- min_x)/(max_x - min_x), (positions[edge[1]][1]- min_y)/(max_y - min_y)),
                        stroke='#000', stroke_width=0.02)
        dwg.add(line)
    dwg.save(pretty=True)
    return 0


# posterior a que el usuario elija un parámetro.
def connected_graph(num_votes):
    check_graph = nx.Graph()
    for node in (vote_global_graph.nodes(data=True)):
        check_graph.add_node(node[0], pos=node[1]['pos'])

    for edge in (vote_global_graph.edges(data=True)):
        if int(edge[2]['votes']) > num_votes:
            check_graph.add_edge(edge[0], edge[1], weight=edge[2]['weight'], votes=edge[2]['votes'])

    draw_graph(check_graph)
    # connected_components_list = list(nx.connected_components(check_graph))
    connected_components_list = sorted(nx.connected_components(check_graph), key=len, reverse=True)
    print(connected_components_list)
    # if the graph is not connected
    flag = True
    if connected_components_list.__len__() > 1:
        for s in range(0, connected_components_list.__len__()-1):
            node_x, node_y, dist = compare_distance_matrix(connected_components_list[0], connected_components_list[1])
            check_graph.add_edge(str(node_x), str(node_y), weight=dist)
            draw_graph(check_graph)
            connected_components_list = sorted(nx.connected_components(check_graph), key=len, reverse=True)
            print(connected_components_list)
    return check_graph


def compare_distance_matrix(component_x, component_y):
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


