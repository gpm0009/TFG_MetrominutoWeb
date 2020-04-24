"""
    metrominuto_app.svgfunctions

    This file contais the operations needed to convert NetworkX graph into
    SVG data.
"""
import math

import networkx as nx
import svgwrite as svg
import numpy as np
from metrominuto_app import globals
# from metrominuto_app import google_maps
import os

colors = ['pink', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple']


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
    vb = str(min_x - radio) + ' ' + str(min_y - radio) + ' ' + str(dif_x + radio) + ' ' + str(dif_y + radio)
    dwg = svg.Drawing(file_name, size=('100%', '100%'),
                      viewBox='0 0.2 1 1.5', profile='full')
    id_color = 0
    for edge in (graph_votes.edges(data=True)):
        color = get_color(id_color)
        id_color = id_color + 1
        if id_color > colors.__len__() - 1:
            id_color = 0
        start_x = 1.4 - (positions[edge[0]][0] - min_x) / dif_x
        start_y = (positions[edge[0]][1] - min_y) / dif_y
        end_x = 1.4 - (positions[edge[1]][0] - min_x) / dif_x
        end_y = (positions[edge[1]][1] - min_y) / dif_y
        line = dwg.line(id='line',
                        start=(start_y, start_x),
                        end=(end_y, end_x),
                        stroke=color, fill=color, stroke_width=0.01)
        xx, yy = calculate_time_position(start_x, start_y, end_x, end_y)
        time = dwg.text(edge[2]['duration'], insert=(yy, xx), stroke='none',
                        fill=color,
                        font_size=str(radio),
                        font_weight="bold",
                        font_family="Arial")

        dwg.add(time)
        dwg.add(line)
    for node in (graph_votes.nodes(data=True)):
        coord_x = 1.4 - (node[1]['pos'][0] - min_x) / dif_x
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
        label = dwg.text('Marcador' + node[0],
                         insert=(coord_y + radio * 1.5, coord_x + radio * 0.2),
                         stroke='none',
                         fill='black',
                         font_size=str(radio),
                         font_weight="bold",
                         font_family="Arial")
        # dwg.add(label)
    dwg.save(pretty=True)
    return 0


def draw(graph_votes):
    positions = nx.get_node_attributes(graph_votes, 'pos')
    coords_x = []
    coords_y = []
    for i in range(0, positions.__len__()):
        coords_x.append(positions[str(i)][0])
        coords_y.append(positions[str(i)][1])
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    dif_x = (max_x - min_x)
    dif_y = (max_y - min_y)
    radio = 0.025  # Nodes radio.
    file_name = 'metrominuto_app/templates/grafo_svg.svg'
    vb = str(min_x - radio) + ' ' + str(min_y - radio) + ' ' + str(dif_x + radio) + ' ' + str(dif_y + radio)
    dwg = svg.Drawing(file_name, size=('100%', '100%'),
                      viewBox='0 0.2 1 1.5', profile='full')
    id_color = 0
    for edge in graph_votes.edges(data=True):
        color = get_color(id_color)
        id_color += 1
        if id_color > colors.__len__() - 1:
            id_color = 0
        start = [1.4 - (positions[edge[0]][0] - min_x) / dif_x, (positions[edge[0]][1] - min_y) / dif_y]
        end = [1.4 - (positions[edge[1]][0] - min_x) / dif_x, (positions[edge[1]][1] - min_y) / dif_y]
        line = add_line(dwg, start, end, color)
        dwg.add(line)
        time_pos = calculate_time_position(start[0], start[1], end[0], end[1])
        time_label = add_label(dwg, time_pos, edge[2]['duration'], radio, color)
        dwg.add(time_label)

    for node in graph_votes.nodes(data=True):
        point = [1.4 - (node[1]['pos'][0] - min_x) / dif_x, (node[1]['pos'][1] - min_y) / dif_y]
        circle = add_circle(dwg, point, radio, node[0])
        dwg.add(circle)
        node_label = add_label(dwg, point, 'Marcador'+node[0], radio, 'black')
        dwg.add(node_label)
        dwg.save(pretty=True)
    return 0


def add_line(dwg, start, end, color):
    return dwg.line(id='line',
                    start=(start[1], start[0]),
                    end=(end[1], end[0]),
                    stroke=color, fill=color, stroke_width=0.01)


def add_label(dwg, pos, text, radio, color):
    return dwg.text(text, insert=(pos[1], pos[0]), stroke='none',
                    fill=color,
                    font_size=str(radio),
                    font_weight="bold",
                    font_family="Arial")


def add_circle(dwg, pos, radio, name):
    return dwg.circle(id='node' + name, center=(pos[1], pos[0]), r=str(radio),
                      fill='black', stroke='white', stroke_width=0.010)


def get_color(cont):
    return colors[cont]


def calculate_time_position(x1, y1, x2, y2):
    pos = []
    vpx = -(y2 - y1)
    vpy = x2 - x1
    dist = np.sqrt(vpx ** 2 + vpy ** 2)
    pm_x = (x1 + x2) / 2
    pm_y = (y1 + y2) / 2
    # x = pm_x - 0.01 * (vpx / dist)
    # y = pm_y - 0.01 * (vpy / dist)
    pos.append(pm_x - 0.01 * (vpx / dist))
    pos.append(pm_y - 0.01 * (vpy / dist))
    return pos
