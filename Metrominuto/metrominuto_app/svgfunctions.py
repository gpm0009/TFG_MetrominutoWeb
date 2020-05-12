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

    def __str__(self):
        return "(" + str(self.p.x) + ", " + str(self.p.y) + ") Base = " + str(self.w) + " Altura = " + str(self.h)


colors = ['pink', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple']


def draw_metrominuto(graph_votes):
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
    lines_points = []
    lines_points_nodes = []
    list_aux = []
    for edge in graph_votes.edges():
        print("Start -> End: ", edge[0], ' | ', edge[1])
        start = Point(positions[edge[0]][0], positions[edge[0]][1])
        end = Point(positions[edge[1]][0], positions[edge[1]][1])
        lines_points = time_discretize(lines_points, start, end)
        list_aux = discretizar_linea_proyeccion(list_aux, start, end, 0.013)
        # if edge[0] == '0' and edge[1] == '5':
        lines_points_nodes = node_discretize(lines_points_nodes, start, end)

    for edge in graph_votes.edges(data=True):
        # print("Start -> End: ", edge[0], ' | ', edge[1])
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
        text_weight, text_height = 0.08, 0.013  # get_text_metrics('Arial', int(radio * 1000), edge[2]['duration'])
        # text_pos = calculate_overlap(text_weight, text_height, start, end, time_pos_negativa, time_pos_positiva)
        # text_pos, points_list = check_points(Point(start[0], start[1]), Point(end[0], end[1]), text_weight, text_height,
        #                                     time_pos_positiva,
        #                                     time_pos_negativa, edge)
        text_pos = discretizar_time_pos(list_aux, text_weight, text_height, time_pos_positiva, time_pos_negativa)
        # for point in points_list:
        #     circle = add_circle(dwg, [point.x, point.y], 0.009, 0, 'disc')
        #     dwg.add(circle)
        time_label = add_label(dwg, text_pos, edge[2]['duration'], radio, color)
        dwg.add(time_label)
        rect = dwg.rect(insert=(text_pos[0], text_pos[1] - text_height), size=(text_weight, text_height),
                        stroke=color, fill=color, stroke_width=0.01)
        # dwg.add(rect)

    for node in graph_votes.nodes(data=True):
        point = [node[1]['pos'][0], node[1]['pos'][1]]
        circle = add_circle(dwg, point, radio, 0.010, node[0])
        dwg.add(circle)
        text_weight, text_height = 0.12, 0.013  # get_text_metrics('Arial', int(radio * 1000), 'Marcador' + node[0])
        # pos_label = node_label_overlap(node, point, radio, text_weight, text_height, graph_votes)
        pos_label = discretizar_nodo(point, radio, text_weight, text_height, list_aux)
        # text_label = google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address']
        node_label = add_label(dwg, pos_label, 'Marcador' + node[0], radio, 'black')
        dwg.add(node_label)
        # rect = dwg.rect(insert=(pos_label[0], pos_label[1] - text_height), size=(text_weight, text_height),
        #                 stroke=color, fill=color, stroke_width=0.01)
        # dwg.add(rect)
        # corner = add_circle(dwg, pos_label, 0.009, 0, 'disc')
        # dwg.add(corner)
        # for point in list_aux:
        #     circle = add_circle(dwg, [point.x, point.y], 0.009, 0, 'disc')
        #     dwg.add(circle)
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


def add_circle(dwg, pos, radio, stroke, name):
    return dwg.circle(id='node' + name, center=(pos[0], pos[1]), r=str(radio),
                      fill='black', stroke='white', stroke_width=stroke)


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


def node_label_overlap(node, point, radio, text_weight, text_height, graph_votes):
    positions = nx.get_node_attributes(graph_votes, 'pos')
    b = 0.01
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

    return [abs(point[0] + radio), point[1] - radio]


def time_discretize(poinsts_list, start, end):
    vector = Point(start.x - end.x, start.y - end.y)
    separacion = 0.009
    pm = Point((end.x + start.x) / 2, (end.y + start.y) / 2)
    if vector.x == 0.0 and vector.y != 0.0:  #vertical
        for y in np.arange(pm.y-separacion*6, pm.y+separacion*6, separacion):
            poinsts_list.append(Point(start.x, y))
    elif vector.y == 0.0 and vector.x != 0.0:  # horizontal
        for x in np.arange(pm.x - separacion * 6, pm.x + separacion * 6, separacion):
            poinsts_list.append(Point(x, start .y))
    else:
        for x in np.arange(pm.x - separacion * 6, pm.x + separacion * 6, separacion):
            y = (((x - start.x) * vector.y) / vector.x) + start.y
            poinsts_list.append(Point(x, y))
    return poinsts_list


def node_discretize(poinsts_list, start, end):
    vector = Point(start.x - end.x, start.y - end.y)
    separacion = 0.009
    pm = Point((end.x + start.x) / 2, (end.y + start.y) / 2)
    if vector.x == 0.0:  # vertical
        if start.y < end.y:  # sube
            origin = start.y
            final = (start.y + pm.y)/2
            origen_f = (end.y + pm.y) / 2
            final_f = end.y
        else:  # baja
            origin = (start.y + pm.y) / 2
            final = start.y
            origen_f = end.y
            final_f = (end.y + pm.y)/2
        for y in np.arange(origin, final, separacion):
            poinsts_list.append(Point(start.x, y))
        for y in np.arange(origen_f, final_f, separacion):
            poinsts_list.append(Point(start.x, y))

    elif vector.y == 0.0:  # horizontal
        if start.x < end.x:  # izq -> derecha
            origin = start.x
            final = (start.x + pm.x)/2
            origen_f = (end.x + pm.x) / 2
            final_f = end.x
        else:  # derecha -> izq
            origin = (start.x + pm.x) / 2
            final = start.x
            origen_f = end.x
            final_f = (end.x + pm.x) / 2
        for x in np.arange(origin, final, separacion):
            poinsts_list.append(Point(x, start.y))
        for x in np.arange(origen_f, final_f, separacion):
            poinsts_list.append(Point(x, start.y))

    else:  # si no es horizontal ni vertical, formula
        if start.x < end.x:  # izq -> derecha
            origin = start.x
            final = (start.x + pm.x)/2
            origen_f = (end.x + pm.x) / 2
            final_f = end.x
        else:
            origin = (start.x + pm.x) / 2
            final = start.x
            origen_f = end.x
            final_f = (end.x + pm.x) / 2
        for x in np.arange(origin, final, separacion):
            y = (((x - start.x) * vector.y) / vector.x) + start.y
            poinsts_list.append(Point(x, y))
        for x in np.arange(origen_f, final_f, separacion):
            y = (((x - start.x) * vector.y) / vector.x) + start.y
            poinsts_list.append(Point(x, y))
    return poinsts_list


def discretizar_time_pos(poinsts_list, text_weight, text_height, time_pos_positiva, time_pos_negativa):
    text_height = text_height+ 0.004
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
    for rect in list_rect_text:
        if not is_over_rect(poinsts_list, rect):
            return [rect.p.x, rect.p.y]
    print('default')
    return 0


def check_points(start, end, text_weight, text_height, time_pos_positiva, time_pos_negativa, edge):
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
    vector = Point(start.x - end.x, start.y - end.y)
    separacion = 0.009
    pm = Point((end.x + start.x) / 2, (end.y + start.y) / 2)
    poinsts_list = []
    if vector.x == 0.0 and vector.y != 0.0:  # vertical
        for y in np.arange(pm.y - separacion * 6, pm.y + separacion * 6, separacion):
            poinsts_list.append(Point(start.x, y))
    elif vector.y == 0.0 and vector.x != 0.0:  # horizontal
        for x in np.arange(pm.x - separacion * 6, pm.x + separacion * 6, separacion):
            poinsts_list.append(Point(x, start.y))
    else:
        for x in np.arange(pm.x - separacion * 6, pm.x + separacion * 6, separacion):
            y = (((x - start.x) * vector.y) / vector.x) + start.y
            poinsts_list.append(Point(x, y))
    for rect in list_rect_text:
        if not is_over_rect(poinsts_list, rect):
            return [rect.p.x, rect.p.y], poinsts_list


def is_over_rect(points_list, rectangle):
    for point in points_list:
        if rectangle.p.x <= point.x <= (rectangle.p.x + rectangle.w) and rectangle.p.y <= point.y <= (rectangle.p.y + rectangle.h):
            return True
    return False


def discretizar_nodo(point, radio, text_weight, text_height, lines_points):
    rect_nodo = Rect(Point(point[0] - radio, point[1] - radio), radio, radio)
    beta = text_height  # 0.013
    list_text_rects = []
    list_text_rects.append(Rect(Point(point[0], point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]+radio+beta, point[1]+radio+beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]+radio+beta, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]+radio+beta, point[1]-radio-beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0], point[1]-radio-beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]-radio-beta, point[1]-radio-beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]-radio-beta-text_weight, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]-radio-beta, point[1]+radio+beta), text_weight, text_height))
    # pos media y final arriba izquierda
    list_text_rects.append(Rect(Point(point[0] - radio - beta - text_weight / 2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio - beta - text_weight, point[1] + radio + beta), text_weight, text_height))
    #pos media y final arriba centro
    list_text_rects.append(Rect(Point(point[0]-text_weight/2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0]-text_weight, point[1] + radio + beta), text_weight, text_height))
    # pos media y final arriba derecha
    list_text_rects.append(Rect(Point(point[0] + radio + beta-text_weight/2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio + beta-text_weight, point[1] + radio + beta), text_weight, text_height))
    # pos media y final abajo derecha
    list_text_rects.append(Rect(Point(point[0] + radio + beta-text_weight/2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio + beta-text_weight, point[1] - radio - beta), text_weight, text_height))
    # pos media y final abajo centro
    list_text_rects.append(Rect(Point(point[0] - text_weight / 2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - text_weight, point[1] - radio - beta), text_weight, text_height))
    # pos media y final abajo izquierda
    list_text_rects.append(Rect(Point(point[0] - radio - beta-text_weight/2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio - beta-text_weight, point[1] - radio - beta), text_weight, text_height))

    for rect in list_text_rects:
        if not is_over_rect(lines_points, rect):
            print([rect.p.x, rect.p.y])
            return [rect.p.x, rect.p.y]
    print('default')
    return [rect_nodo.x - text_weight, rect_nodo.y]


def discretizar_linea_proyeccion(poinsts_list, start, end, text_height=0.013):
    vector_recta = Point(start.x - end.x, start.y - end.y)
    vector_origen = Point(start.x-end.x, 0)
    angulo = np.arccos(abs(vector_recta.x * vector_origen.x + vector_recta.y * vector_origen.y)/(np.sqrt(vector_recta.x**2+vector_recta.y**2)+np.sqrt(vector_origen.x**2+vector_origen.y**2)))
    separacion = text_height * np.cos(angulo)
    if vector_recta.x == 0.0:  # vertical
        if start.y < end.y:  # sube
            origin = start.y
            final = end.y
        else:  # baja
            origin = end.y
            final = start.y
        for y in np.arange(origin, final, text_height-0.003):
            poinsts_list.append(Point(start.x, y))

    elif vector_recta.y == 0.0:  # horizontal
        if start.x < end.x:  # izq -> derecha
            origin = start.x
            final = end.x
        else:  # derecha -> izq
            origin = end.x
            final = start.x
        for x in np.arange(origin, final, separacion-0.003):
            poinsts_list.append(Point(x, start.y))

    else:  # si no es horizontal ni vertical, formula
        if start.x < end.x:  # izq -> derecha
            origin = start.x
            final = end.x
        else:
            origin = end.x
            final = start.x
        for x in np.arange(origin, final, separacion):
            y = (((x - start.x) * vector_recta.y) / vector_recta.x) + start.y
            poinsts_list.append(Point(x, y))

    return poinsts_list
