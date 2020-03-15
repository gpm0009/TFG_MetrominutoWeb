from random import sample
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import globals


def calculate_graph(dista, nodes):
    graph = nx.Graph()
    min_graph = nx.Graph()
    # vote_graph = nx.Graph()
    nodes_name = 0

    for node in nodes:
        graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        min_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        globals.vote_global_graph.add_node(str(nodes_name), pos=(node['position']['lat'], node['position']['lng']))
        nodes_name = nodes_name + 1

    for i in range(0, dista.__len__()):
        for j in range(0, dista.__len__()):
            if i != j:
                graph.add_edge(str(i), str(j), weight=dista[i][j])
    weight = nx.get_edge_attributes(graph, 'weight')
    votes = nodes_votes(graph, nodes_name, min_graph, weight)
    # draw_votes_graph(votes)
    # svg_f.save_svg()
    return votes


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
            globals.vote_global_graph.add_edge(random_graph[z][0], random_graph[z][1],
                                       weight=weight[(random_graph[z][0], random_graph[z][1])],
                                       votes=votes[x, y] + 1)
    print(votes)
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
    nx.draw_networkx(globals.vote_global_graph, pos=nx.get_node_attributes(globals.vote_global_graph, 'pos'), node_color='#80b41f')
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
    check_graph = nx.Graph()
    for node in (globals.vote_global_graph.nodes(data=True)):
        check_graph.add_node(node[0], pos=node[1]['pos'])

    for edge in (globals.vote_global_graph.edges(data=True)):
        if int(edge[2]['votes']) > num_votes:
            check_graph.add_edge(edge[0], edge[1], weight=edge[2]['weight'], votes=edge[2]['votes'])

    connected_components_list = sorted(nx.connected_components(check_graph), key=len, reverse=True)
    print(connected_components_list)
    # if the graph is not connected
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