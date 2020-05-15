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


class Color:
    def __init__(self):
        self.cont_green = 0
        self.cont_red = 0
        self.cont_blue = 0
        self.cont_purple = 0
        self.cont_brown = 0
        self.green = ['#31a84f', '#259f48', '#179740', '#008f39', '#008732', '#007f2a', '#007723']
        self.red = ['#e52b15', '#dc210e', '#d41406', '#cc0000', '#c40000', '#bc0000', '#b40000']
        self.blue = ['#3d9fe7', '#2f87de', '#1f8fd5', '#0087cc', '#007fc3', '#0077bb', '#006fb2']
        self.purple = ['#905996', '#8a5390', '#844e8a', '#7e4884', '#78427e', '#723d78', '#6c3873']
        self.brown = ['#ab6b49', '#a36543', '#9c5e3d', '#955837', '#8e5231', '#874c2b', '#804626']

    def get_color(self, time_str):
        time = int(time_str.split(' mins')[0]) or int(time_str.split(' hours')[0])
        if time <= 5:
            return_color = self.green[self.cont_green]
            self.cont_green += 1
        elif time <= 8:
            return_color = self.brown[self.cont_brown]
            self.cont_brown += 1
        elif time <= 12:
            return_color = self.purple[self.cont_purple]
            self.cont_purple += 1
        elif time <= 12:
            return_color = self.blue[self.cont_blue]
            self.cont_blue += 1
        else:
            return_color = self.red[self.cont_red]
            self.cont_red += 1
        return return_color


colors = ['pink', 'orange', 'red', 'brown', 'green', 'blue', 'grey', 'purple']


def draw_metrominuto(graph_votes):
    """Functions that save graph as SVG.
        :param graph_votes: Graph that contais all data about nodes and edges.
        :type graph_votes: NetworkX graph
        :return: svg element.
        :rtype: str.
        """
    var_color = Color()
    positions = nx.get_node_attributes(graph_votes, 'pos')
    radio = 0.025  # Nodes radio.
    file_name = 'metrominuto_app/templates/grafo_svg.svg'
    # vb = str(min_x - radio) + ' ' + str(min_y - radio) + ' ' + str(dif_x + radio) + ' ' + str(dif_y + radio)
    dwg = svg.Drawing(file_name, size=('100%', '100%'), viewBox='0 0.2 1 1.5', profile='full')
    id_color = 0
    lines_points = []
    for edge in graph_votes.edges():
        start = Point(positions[edge[0]][0], positions[edge[0]][1])
        end = Point(positions[edge[1]][0], positions[edge[1]][1])
        lines_points = discretizar_linea_proyeccion(lines_points, start, end, 0.013)

    for edge in graph_votes.edges(data=True):
        # print("Start -> End: ", edge[0], ' | ', edge[1])
        color = get_color(id_color)
        id_color += 1
        if id_color > colors.__len__() - 1:
            id_color = 0
        start = [positions[edge[0]][0], positions[edge[0]][1]]
        end = [positions[edge[1]][0], positions[edge[1]][1]]
        color_aux = var_color.get_color(edge[2]['duration'])
        # Linea entre nodos
        line = add_line(dwg, start, end, color_aux)
        dwg.add(line)
        # punto de la recta perpendicular.
        time_pos_positiva, time_pos_negativa = calculate_time_position(start[0], start[1], end[0], end[1])
        # weight and height text.
        text_weight, text_height = 0.08, 0.013  # get_text_metrics('Arial', int(radio * 1000), edge[2]['duration'])
        text_pos = calculate_time_overlap(lines_points, text_weight, text_height, time_pos_positiva, time_pos_negativa)
        # for point in lines_points:
        #     circle = add_circle(dwg, [point.x, point.y], 0.009, 0, 'disc')
        #     dwg.add(circle)
        time_label = add_label(dwg, text_pos, edge[2]['duration'], radio, color_aux)
        dwg.add(time_label)
        # rect = dwg.rect(insert=(text_pos[0], text_pos[1] - text_height), size=(text_weight, text_height),
        #                 stroke=color, fill=color, stroke_width=0.01)
        # dwg.add(rect)

    for node in graph_votes.nodes(data=True):
        point = [node[1]['pos'][0], node[1]['pos'][1]]
        circle = add_circle(dwg, point, radio, 0.010, node[0])
        dwg.add(circle)
        text_weight, text_height = 0.12, 0.013  # get_text_metrics('Arial', int(radio * 1000), 'Marcador' + node[0])
        # pos_label = node_label_overlap(node, point, radio, text_weight, text_height, graph_votes)
        pos_label = calculate_node_overlap(point, radio, text_weight, text_height, lines_points)
        # text_label = google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address']
        node_label = add_label(dwg, pos_label, 'Marcador' + node[0], radio, 'black')
        dwg.add(node_label)
        # rect = dwg.rect(insert=(pos_label[0], pos_label[1] - text_height), size=(text_weight, text_height),
        #                 stroke=color, fill=color, stroke_width=0.01)
        # dwg.add(rect)
        # for point in lines_points:
        #     circle = add_circle(dwg, [point.x, point.y], 0.009, 0, 'disc')
        #     dwg.add(circle)
    dwg.save(pretty=True)
    # for point in lines_points:
    #     circle = add_circle(dwg, [point.x, point.y], 0.009, 0, 'disc')
    #     dwg.add(circle)
    return dwg.tostring()


def add_line(dwg, start, end, color):
    """Function that adds a label to SVG.
    :param dwg: SVG data.
    :type dwg: svgwrite.
    :param start: Start point of the line.
    :type start: Array.
    :param end: End point of the line.
    :type end: Array
    :param color: color.
    :type color: str.
    :return: svgwrite line element.
    :rtype: svgwrite.
    """
    return dwg.line(id='line',
                    start=(start[0], start[1]),
                    end=(end[0], end[1]),
                    stroke=color, fill=color, stroke_width=0.01)


def add_label(dwg, pos, text, radio, color):
    """Function that adds a label to SVG.
    :param dwg: SVG data.
    :type dwg: svgwrite.
    :param pos: label position. Left bottom corner.
    :type pos: Array.
    :param text: Text to be print in SVG.
    :type text: str.
    :param radio: text font size.
    :type radio: float.
    :param color: color.
    :type color: str.
    :return: svgwrite text element.
    :rtype: svgwrite.
    """
    return dwg.text(text, insert=(pos[0], pos[1]), stroke='none',
                    fill=color,
                    font_size=str(radio),
                    font_weight="bold",
                    font_family="Arial")  # text_anchor='middle'


def add_circle(dwg, pos, radio, stroke, name):
    """Function that adds a circle to SVG.
    :param dwg: SVG data.
    :type dwg: svgwrite.
    :param pos: Circle's center.
    :type pos: Array.
    :param radio: radio of the circle that represents the Node.
    :type radio: float.
    :param stroke: line stroke.
    :type stroke: float.
    :param name: Text to be print in SVG.
    :type name: str.
    :return: svgwrite circle element.
    :rtype: svgwrite.
    """
    return dwg.circle(id='node' + name, center=(pos[0], pos[1]), r=str(radio),
                      fill='black', stroke='white', stroke_width=stroke)


def get_color(cont):
    return colors[cont]


def calculate_time_position(x1, y1, x2, y2):
    """Function that calculate mid point between 2 points and give it some distance from the line. To the positive and
    negative side.
    :param x1:
    :param y1:
    :param x2:
    :param y2:
    :return:
    """
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


def calculate_time_overlap(poinsts_list, text_weight, text_height, time_pos_positiva, time_pos_negativa):
    """Function that calculate is time label overlap with something.
    :param poinsts_list: list of points.
    :type poinsts_list: List.
    :param text_weight: Text weight.
    :type text_weight: float.
    :param text_height: Text height.
    :type text_height: float.
    :param time_pos_positiva: position on positive side of the edge.
    :type time_pos_positiva: Array.
    :param time_pos_negativa: position on the negative side of the line.
    :type time_pos_negativa: Array
    :return: label time position.
    :rtype: Array
    """
    text_height = text_height + 0.004
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
            poinsts_list.append(Point(rect.p.x + text_weight, rect.p.y + text_height))
            poinsts_list.append(Point(rect.p.x + text_weight, rect.p.y))
            poinsts_list.append(Point(rect.p.x, rect.p.y + text_height))
            poinsts_list.append(Point(rect.p.x, rect.p.y))
            return [rect.p.x, rect.p.y]
    # print('default')
    return 0


def is_over_rect(points_list, rectangle):
    """ FUncion that check if some point of a list is inside a rectagle.
    :param points_list: list of points.
    :type: list.
    :param rectangle: rectangle that represent text.
    :type rectangle: Rect.
    :return: if there is one point inside the rectagle, return True.
    :rtype: Boolean.
    """
    for point in points_list:
        if rectangle.p.x <= point.x <= (rectangle.p.x + rectangle.w) and rectangle.p.y <= point.y <= (rectangle.p.y + rectangle.h):
            return True
    return False


def calculate_node_overlap(point, radio, text_weight, text_height, lines_points):
    """ Funcion that calculate if node's label overlap something.
    :param point: Node origin.
    :type point: Point.
    :param radio: radio of the circle that represents the Node.
    :type radio: float.
    :param text_weight: Text weight.
    :type text_weight: float.
    :param text_height: Text height.
    :type text_height: float.
    :param lines_points: list of points.
    :type lines_points: list.
    :return: label position.
    :rtype: array.
    """
    rect_nodo = Rect(Point(point[0] - radio, point[1] - radio), radio, radio)
    beta = text_height + 0.006  # 0.013
    text_weight = text_weight + 0.01
    # point[1] = point[1] + text_height
    list_text_rects = []
    list_text_rects.append(Rect(Point(point[0], point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio + beta, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio + beta, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] + radio, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0], point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio - beta, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio - beta - text_weight, point[1]), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - radio - beta, point[1] + radio + beta), text_weight, text_height))
    # pos media y final arriba izquierda
    list_text_rects.append(
        Rect(Point(point[0] - radio - beta - text_weight / 2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(
        Rect(Point(point[0] - radio - beta - text_weight, point[1] + radio + beta), text_weight, text_height))
    # pos media y final arriba centro
    list_text_rects.append(Rect(Point(point[0] - text_weight / 2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - text_weight, point[1] + radio + beta), text_weight, text_height))
    # pos media y final arriba derecha
    list_text_rects.append(
        Rect(Point(point[0] + radio + beta - text_weight / 2, point[1] + radio + beta), text_weight, text_height))
    list_text_rects.append(
        Rect(Point(point[0] + radio + beta - text_weight, point[1] + radio + beta), text_weight, text_height))
    # pos media y final abajo derecha
    list_text_rects.append(
        Rect(Point(point[0] + radio + beta - text_weight / 2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(
        Rect(Point(point[0] + radio + beta - text_weight, point[1] - radio - beta), text_weight, text_height))
    # pos media y final abajo centro
    list_text_rects.append(Rect(Point(point[0] - text_weight / 2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(Rect(Point(point[0] - text_weight, point[1] - radio - beta), text_weight, text_height))
    # pos media y final abajo izquierda
    list_text_rects.append(
        Rect(Point(point[0] - radio - beta - text_weight / 2, point[1] - radio - beta), text_weight, text_height))
    list_text_rects.append(
        Rect(Point(point[0] - radio - beta - text_weight, point[1] - radio - beta), text_weight, text_height))

    for rect in list_text_rects:
        if not is_over_rect(lines_points, rect):
            lines_points.append(Point(rect.p.x + text_weight, rect.p.y + text_height))
            lines_points.append(Point(rect.p.x + text_weight, rect.p.y))
            lines_points.append(Point(rect.p.x, rect.p.y + text_height))
            lines_points.append(Point(rect.p.x, rect.p.y))
            return [rect.p.x, rect.p.y]
    print('default')
    return [rect_nodo.x - text_weight, rect_nodo.y]


def discretizar_linea_proyeccion(poinsts_list, start, end, text_height=0.013):
    """ Function that calculates points on lines. Discretize edges.
    :param poinsts_list: List of discretized points, including rectangle's corner.
    :type poinsts_list: list
    :param start: Start Point of the line.
    :type start: Point.
    :param end: End Point of the line.
    :type end: Point
    :param text_height: Text height.
    :type text_height: float
    :return: List of points belonging to the edges.
    :rtype: List
    """
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
        for x in np.arange(origin, final, text_height-0.003):
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

