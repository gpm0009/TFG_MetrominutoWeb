"""
    metrominuto_app.svgfunctions

    This file contais the operations needed to convert NetworkX graph into
    SVG data.
"""
import math
# import tkinter as Tkinter
# import tkinter.font as tkFont
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

    radio = 0.025  # Nodes radio.
    file_name = 'metrominuto_app/templates/grafo_svg.svg'
    # vb = str(min_x - radio) + ' ' + str(min_y - radio) + ' ' + str(dif_x + radio) + ' ' + str(dif_y + radio)
    dwg = svg.Drawing(file_name, size=('100%', '100%'), viewBox='0 0.2 1 1.5', profile='full')
    id_color = 0
    for edge in graph_votes.edges(data=True):
        print("Start -> End: ", edge[0], ' | ', edge[1])
        color = get_color(id_color)
        id_color += 1
        if id_color > colors.__len__() - 1:
            id_color = 0
        start = [positions[edge[0]][0], positions[edge[0]][1]]
        end = [positions[edge[1]][0], positions[edge[1]][1]]
        # Linea entre nodos
        line = add_line(dwg, start, end, color)
        dwg.add(line)
        # punto de la recta perpendicular.
        time_pos_positiva, time_pos_negativa = calculate_time_position(start[0], start[1], end[0], end[1])
        # weight and height text.
        text_weight, text_height = 0.096, 0.038  # get_text_metrics('Arial', int(radio * 1000), edge[2]['duration'])
        text_pos = calculate_overlap(text_weight, text_height, start, end, time_pos_negativa, time_pos_positiva)
        print('POSICIÓN = ', text_pos)
        time_label = add_label(dwg, text_pos, edge[2]['duration'], radio, color)
        dwg.add(time_label)

        # dibujo rectangulo texto
        rect = dwg.rect(insert=(text_pos[0], text_pos[1] - text_height),
                        size=(text_weight, text_height),
                        stroke=color, fill=color, stroke_width=0.01)
        # dwg.add(rect)
        # line_pm_text = add_line(dwg, time_pos_negativa, pm, 'black')
        # dwg.add(line_pm_text)
        # Rectangulo recta. Punto esquina inferior izquierda
        # rect_linea = Rect(Point(pm[1], pm[0]), abs(end[1] - pm[1]), end[0] - pm[0])

    for node in graph_votes.nodes(data=True):
        point = [node[1]['pos'][0], node[1]['pos'][1]]
        circle = add_circle(dwg, point, radio, node[0])
        dwg.add(circle)
        text_weight, text_height = 0.12, 0.038  # get_text_metrics('Arial', int(radio * 1000), 'Marcador' + node[0])
        pos_label = node_label_overlap(node, point, radio, text_weight, text_height, graph_votes)
        # text_label = google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address']
        node_label = add_label(dwg, pos_label, 'Marcador' + node[0], radio, 'black')
        dwg.add(node_label)
    dwg.save(pretty=True)
    return dwg.tostring()


def add_line(dwg, start, end, color):
    return dwg.line(id='line',
                    start=(start[0], start[1]),
                    end=(end[0], end[1]),
                    stroke=color, fill=color, stroke_width=0.01)


def add_label(dwg, pos, text, radio, color):
    return dwg.text(text, insert=(pos[0], pos[1]), stroke='none',
                    fill=color,
                    font_size=str(radio),
                    font_weight="bold",
                    font_family="Arial")  # text_anchor='middle'


def add_circle(dwg, pos, radio, name):
    return dwg.circle(id='node' + name, center=(pos[0], pos[1]), r=str(radio),
                      fill='black', stroke='white', stroke_width=0.010)


def get_color(cont):
    return colors[cont]


def dist_point_to_point(a, b):
    return np.sqrt(abs(a[0] - b[0]) ** 2 + abs(a[1] - b[1]) ** 2)


def calculate_time_position(x1, y1, x2, y2):
    pos_negative = []
    pos_positive = []
    vpx = -(y2 - y1)
    vpy = x2 - x1
    dist = np.sqrt(vpx ** 2 + vpy ** 2)
    pm_x = (x1 + x2) / 2
    pm_y = (y1 + y2) / 2
    pos_negative.append(pm_x - 0.025 * (vpx / dist))
    pos_negative.append(pm_y - 0.025 * (vpy / dist))
    pos_positive.append(pm_x + 0.025 * (vpx / dist))
    pos_positive.append(pm_y + 0.025 * (vpy / dist))
    return pos_negative, pos_positive


# def get_text_metrics(family, size, text):
# initialize Tk so that font metrics will work
# tk_root = Tkinter.Tk()
# font = None
#  key = (family, size)
#  font = Tkinter.font.Font(family=family, size=size)
# #  assert font is not None
# (w, h) = (font.measure(text), font.metrics('linespace'))
#  return w / 1000, h / 1000


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def distance(self, p):
        return math.sqrt(abs(p.x - self.x) ** 2 + abs(p.y - self.y) ** 2)


class Rect:
    def __init__(self, p, w=0, h=0):
        self.p = p
        self.w = w
        self.h = h

    def collide(self, r):
        # calculamos los valores de los lados
        left = self.p.x
        right = self.p.y + self.w
        top = self.p.y + self.h
        bottom = self.p.y
        r_left = r.p.x
        r_right = r.p.x + r.w
        r_top = r.p.y + r.h
        r_bottom = r.p.y
        return right >= r_left and left <= r_right and top >= r_bottom and bottom <= r_top


def calculate_overlap(text_weight, text_height, start, end, time_pos_negativa, time_pos_positiva):
    pm = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
    weight_rect = abs(end[0] - pm[0])
    height_rect = abs(end[1] - pm[1])

    list_rect_text = [Rect(Point(time_pos_negativa[0], time_pos_negativa[1]), text_weight, text_height),
                      Rect(Point(time_pos_negativa[0] - text_weight / 2, time_pos_negativa[1]), text_weight,
                           text_height),
                      Rect(Point(time_pos_negativa[0] - text_weight, time_pos_negativa[1]), text_weight, text_height),
                      Rect(Point(time_pos_negativa[0] - text_weight, time_pos_negativa[1] - text_height / 2),
                           text_weight,
                           text_height),
                      Rect(Point(time_pos_negativa[0] - text_weight, time_pos_negativa[1] - text_height), text_weight,
                           text_height),
                      Rect(Point(time_pos_negativa[0] - text_weight / 2, time_pos_negativa[1] - text_height),
                           text_weight,
                           text_height),
                      Rect(Point(time_pos_negativa[0], time_pos_negativa[1] - text_height), text_weight, text_height),
                      Rect(Point(time_pos_negativa[0], time_pos_negativa[1] - text_height / 2), text_weight,
                           text_height),
                      Rect(Point(time_pos_positiva[0], time_pos_positiva[1]), text_weight, text_height),
                      Rect(Point(time_pos_positiva[0] + text_weight / 2, time_pos_positiva[1]), text_weight,
                           text_height),
                      Rect(Point(time_pos_positiva[0] + text_weight, time_pos_positiva[1]), text_weight, text_height),
                      Rect(Point(time_pos_positiva[0] + text_weight, time_pos_positiva[1] + text_height / 2),
                           text_weight,
                           text_height),
                      Rect(Point(time_pos_positiva[0] + text_weight, time_pos_positiva[1] + text_height), text_weight,
                           text_height),
                      Rect(Point(time_pos_positiva[0] + text_weight / 2, time_pos_positiva[1] + text_height),
                           text_weight,
                           text_height),
                      Rect(Point(time_pos_positiva[0], time_pos_positiva[1] + text_height), text_weight, text_height),
                      Rect(Point(time_pos_positiva[0], time_pos_positiva[1] + text_height / 2), text_weight,
                           text_height)]

    rect_right_top = Rect(Point(pm[0], pm[1]), weight_rect, height_rect)
    rect_right_bottom = Rect(Point(pm[0], pm[1] - height_rect), weight_rect, height_rect)
    rect_left_top = Rect(Point(pm[0], pm[1] - height_rect), weight_rect, height_rect)
    rect_left_bottom = Rect(Point(pm[0] - weight_rect, pm[1] - height_rect), weight_rect, height_rect)
    list_rect = []
    if start[0] < end[0] and abs(end[1] - start[1]) > 0.004:  # izq derecha
        if end[1] < start[1]:  # sube
            list_rect.append(rect_left_bottom)
            list_rect.append(rect_right_top)
        else:
            list_rect.append(rect_left_top)
            list_rect.append(rect_right_bottom)
    elif start[0] > end[0] and abs(end[1] - start[1]) > 0.004:
        if end[1] < start[1]:  # sube
            list_rect.append(rect_right_bottom)
            list_rect.append(rect_left_top)
        else:
            list_rect.append(rect_right_bottom)
            list_rect.append(rect_right_top)
    else:
        return time_pos_negativa

    for rect_text in list_rect_text:
        for rect_line in list_rect:
            if not rect_text.collide(rect_line):
                return [rect_text.p.x, rect_text.p.y]

    return 0


def node_label_overlap(node, point, radio, text_weight, text_height, graph_votes):
    positions = nx.get_node_attributes(graph_votes, 'pos')

    point_rect = Rect(Rect(Point(point[1], point[0]), radio, radio))
    list_text_rects = []
    # 8 esquinas alrededor del punto.
    list_text_rects.append(Rect(Point(point[0] + radio, point[1] + radio), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio, point[1] - radio), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0], point[1] - radio), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio, point[1] - radio), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio, point[1] + radio), text_weight, text_height))

    edge_list_rects = []
    start = [positions[node[0]][0], positions[node[0]][1]]
    for edge in graph_votes.edges(node[0], data=True):
        end = [positions[edge[1]][0], positions[edge[1]][1]]
        pm = [(start[0] + end[0]) / 2, (start[1] + end[1]) / 2]
        weight_rect = abs(end[0] - pm[0])
        height_rect = abs(end[1] - pm[1])
        rect_right_top = Rect(Point(pm[0], pm[1]), weight_rect, height_rect)
        rect_right_bottom = Rect(Point(pm[0], pm[1] - height_rect), weight_rect, height_rect)
        rect_left_top = Rect(Point(pm[0], pm[1] - height_rect), weight_rect, height_rect)
        rect_left_bottom = Rect(Point(pm[0] - weight_rect, pm[1] - height_rect), weight_rect, height_rect)
        if start[0] < end[0] and abs(end[1] - start[1]) > 0.004:  # izq derecha
            if end[1] < start[1]:  # sube
                edge_list_rects.append(rect_left_bottom)
            else:
                edge_list_rects.append(rect_left_top)
        elif start[0] > end[0] and abs(end[1] - start[1]) > 0.004:
            if end[1] < start[1]:  # sube
                edge_list_rects.append(rect_right_bottom)
            else:
                edge_list_rects.append(rect_right_top)

    for rect_text in list_text_rects:
        for rect_line in edge_list_rects:
            if not rect_text.collide(rect_line):
                return [rect_text.p.x, rect_text.p.y]

    return [point[0] + radio, point[1] - radio]