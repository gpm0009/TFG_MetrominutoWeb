"""
    metrominuto_app.svgfunctions

    This file contais the operations needed to convert NetworkX graph into
    SVG data.
"""
import networkx as nx
import svgwrite as svg
from metrominuto_app import globals
# from metrominuto_app import google_maps
import os


def generate_svg(graph_votes):
    """Functions that save graph as SVG.

    :param graph_votes: Graph that contais all data about nodes and edges.
    :type graph_votes: NetworkX graph

    :return:
    """
    positions = nx.get_node_attributes(graph_votes, 'pos')
    coords_x = []
    coords_y = []
    for x in range(0, positions.__len__()):
        coords_x.append(positions[str(x)][0])
        coords_y.append(positions[str(x)][1])
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    dif_x = (max_x - min_x)
    dif_y = (max_y - min_y)
    # print(max_x, min_x, max_y, min_y)
    radio = 0.025
    file_name = 'metrominuto_app/templates/grafo_svg.svg'
    vb = str(min_x-radio) + ' ' + str(min_y-radio) + ' ' + str(dif_x+radio) + ' ' + str(dif_y+radio)
    dwg = svg.Drawing(file_name, size=('100%', '100%'),
                      viewBox='0 0.2 1 1.5', profile='full')
    id_color = 0
    for edge in (graph_votes.edges(data=True)):
        color = select_color(id_color)
        id_color = id_color + 1
        if id_color > colors.__len__()-1:
            id_color = 0
        start_x = 1.4-(positions[edge[0]][0] - min_x) / dif_x
        start_y = (positions[edge[0]][1] - min_y) / dif_y
        end_x = 1.4-(positions[edge[1]][0] - min_x) / dif_x
        end_y = (positions[edge[1]][1] - min_y) / dif_y
        line = dwg.line(id='line',
                        start=(start_y, start_x),
                        end=(end_y, end_x),
                        stroke=color, fill=color, stroke_width=0.01)
        medio_x, medio_y = mid_point(start_x, start_y, end_x, end_y)
        time = dwg.text(edge[2]['duration'], insert=(medio_y + radio * 1.5, medio_x), stroke='none',
                        fill=color,
                        font_size=str(radio),
                        font_weight="bold",
                        font_family="Arial")

        dwg.add(time)
        dwg.add(line)
    for node in (graph_votes.nodes(data=True)):
        coord_x = 1.4-(node[1]['pos'][0] - min_x) / dif_x
        coord_y = (node[1]['pos'][1] - min_y) / dif_y
        circle = dwg.circle(id='node' + node[0], center=(coord_y, coord_x), r=str(radio),
                            fill='black', stroke='white', stroke_width=0.010)
        dwg.add(circle)
        # label = dwg.text(google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address'],
        #                  insert=(coord_y + radio * 1.5, coord_x + radio * 0.2),
        #                  stroke='none',
        #                  fill='black',
        #                  font_size=str(radio),
        #                  font_weight="bold",
        #                  font_family="Arial")
        # dwg.add(label)
        check_directions(node, node[1]['pos'][0], node[1]['pos'][1])
        label = dwg.text('Marcador'+node[0],
                         insert=(coord_y + radio * 1.5, coord_x + radio * 0.2),
                         stroke='none',
                         fill='black',
                         font_size=str(radio),
                         font_weight="bold",
                         font_family="Arial")
        dwg.add(label)
    dwg.save(pretty=True)
    return 0


def mid_point(c_x, c_y, c_xx, c_yy):
    x = (c_x + c_xx) / 2
    y = (c_y + c_yy) / 2
    return x, y


colors = ['pink', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple']


def select_color(cont):
    color = colors[cont]
    return color


def check_directions(node, pos_x, pos_y):
    graph_nodes = list(globals.vote_global_graph.nodes(data=True)) #graph_nodes[1][0]
    neighbors = []
    for n in globals.vote_global_graph.neighbors(node[0]):
        neighbors.append(n)
    print('Padre:', node[0])
    print('\tVecino: ', neighbors)
    direction = ''
    arriba = False
    derecha = False
    izquierda = False
    abajo = False
    for neighbors in neighbors:
        if graph_nodes[0][1]['pos'][0] >= pos_x and graph_nodes[0][1]['pos'][1] > pos_y:
            arriba = True
            derecha = True
        elif graph_nodes[0][1]['pos'][0] > pos_x and graph_nodes[0][1]['pos'][1] < pos_y:
            abajo = True
            derecha = True

    return 0
