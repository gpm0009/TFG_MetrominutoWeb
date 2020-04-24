"""
    metrominuto_app.svgfunctions

    This file contais the operations needed to convert NetworkX graph into
    SVG data.
"""
import math
import tkinter.font as tkFont
import tkinter as Tkinter
import networkx as nx
import svgwrite as svg
import numpy as np
from metrominuto_app import globals
# from metrominuto_app import google_maps
import os

colors = ['pink', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple']


def draw(graph_votes):
    """Functions that save graph as SVG.

        :param graph_votes: Graph that contais all data about nodes and edges.
        :type graph_votes: NetworkX graph

        :return:
        """
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
        w, h = get_text_metrics('Arial', int(radio * 1000), edge[2]['duration'])
        l1 = Point(start[1] + 0.01, start[0])  # top izquierda
        r1 = Point(end[1], end[0] + 0.01)  # bottom derecha
        l2 = Point(time_pos[1], time_pos[0] - h)  # top izquierda
        r2 = Point(time_pos[1] + w, time_pos[0])  # bottom derecha
        rect = dwg.rect(insert=(time_pos[1], time_pos[0]-h), size=(w, h),
                        stroke=color, fill=color, stroke_width=0.01)
        dwg.add(rect)
        if doOverlap(l1, r1, l2, r2):
            print("Rectangles Overlap : ", edge[0], ' | ', edge[1])
        else:
            print("Rectangles Don't Overlap")
    for node in graph_votes.nodes(data=True):
        point = [1.4 - (node[1]['pos'][0] - min_x) / dif_x, (node[1]['pos'][1] - min_y) / dif_y]
        circle = add_circle(dwg, point, radio, node[0])
        dwg.add(circle)
        # text_label = google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address']
        node_label = add_label(dwg, point, 'Marcador' + node[0], radio, 'black')
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
                    font_family="Arial")  # text_anchor='middle'


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
    pos.append(pm_x - 0.02 * (vpx / dist))
    pos.append(pm_y - 0.02 * (vpy / dist))
    return pos


def get_text_metrics(family, size, text):
    # initialize Tk so that font metrics will work
    tk_root = Tkinter.Tk()
    font = None
    key = (family, size)
    font = tkFont.Font(family=family, size=size)
    assert font is not None
    (w, h) = (font.measure(text), font.metrics('linespace'))
    return w / 1000, h / 1000


# Returns true if two rectangles(l1, r1)
# and (l2, r2) overlap
def doOverlap(l1, r1, l2, r2):
    # If one rectangle is on left side of other
    if l1.x >= r2.x or l2.x >= r1.x:
        return False

    # If one rectangle is above other
    if l1.y <= r2.y or l2.y <= r1.y:
        return False

    return True


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
