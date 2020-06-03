import math


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
        self.check_cont()
        if time_str != '':
            time = int(time_str.split(' mins')[0]) or int(time_str.split(' hours')[0])
        else:
            time = 20
        if time <= 5:
            return_color = self.green[self.cont_green]
            self.cont_green += 1
        elif time <= 7:
            return_color = self.brown[self.cont_brown]
            self.cont_brown += 1
        elif time <= 10:
            return_color = self.purple[self.cont_purple]
            self.cont_purple += 1
        elif time <= 13:
            return_color = self.blue[self.cont_blue]
            self.cont_blue += 1
        else:
            return_color = self.red[self.cont_red]
            self.cont_red += 1
        return return_color

    def check_cont(self):
        if self.cont_red > self.red.__len__() - 1:
            self.cont_red = 0
        if self.cont_green > self.green.__len__() - 1:
            self.cont_green = 0
        if self.cont_blue > self.blue.__len__() - 1:
            self.cont_blue = 0
        if self.cont_purple > self.purple.__len__() - 1:
            self.cont_purple = 0
        if self.cont_brown > self.brown.__len__() - 1:
            self.cont_brown = 0


class Graphs:
    """
    Class that represents and create graph structure in order to pass it to the views.
    """
    def __init__(self):
        """
        Graphs class init.
        :param nodes: List that contains nodes with their attributes.
        :type nodes: list.
        :param edges: List that contains edges and ther attributes.
        :type edges: list.
        :param labels_nodes: List that contains node labels and their positions.
        :type labels_nodes: list.
        :param labels_edges: List that contains edge labels and their positions.
        :type labels_edges: list.
        """
        self.nodes = []
        self.edges = []
        self.labels_nodes = []
        self.labels_edges = []

    def add_nodes(self, node):
        """
        Method that adds a node to the Graph.
        :param node: list with node attributes.
        :type node: list.
        """
        self.nodes.append({'id': node[0], 'pos': [node[1]['pos'][0], node[1]['pos'][1]]})

    def add_nodes_aux(self, node):
        """
        Method that adds a node form view graph to the Graph.
        :param node: Node with attributes.
        :type node: dict.
        """
        self.nodes.append({'id': node['id'], 'pos': node['pos']})

    def add_edges(self, edge, color, position):
        """
        Method that adds edge to the Graph.
        :param edge: node origin and node end
        :type edge: list.
        :param color: edge's color.
        :type color: Color.
        :param position: Start's and End's Node positions.
        :type position: list.
        """
        self.edges.append(
            {'edge': [edge[0], edge[1]], 'color': color, 'pos': position, 'duration': edge[2]['duration']})

    def add_edges_aux(self, edge):
        """
        Method that adds edge from view to the Graph.
        :param edge: Edge with attributes.
        :type edge: dict.
        """
        self.edges.append(
            {'edge': [edge['edge'][0], edge['edge'][1]], 'color': edge['color'], 'pos': edge['pos'], 'duration': edge['duration']})

    def add_labels(self, g_labels_nodes, g_labels_edges):
        """
        Method that adds labels the Graph.
        :param g_labels_nodes: list with node's labels and positions.
        :type g_labels_nodes: list.
        :param g_labels_edges: list with edge's labels and positions.
        :type g_labels_edges: list.
        """
        for label_node in g_labels_nodes:
            self.labels_nodes.append(label_node)
        for label_edge in g_labels_edges:
            self.labels_edges.append(label_edge)