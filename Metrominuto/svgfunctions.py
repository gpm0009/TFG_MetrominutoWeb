import networkx as nx
import svgwrite as svg
from app import google_maps


def save_svg():
    dwg = svg.Drawing('templates/test.svg', size=("800px", "600px"), profile='full')
    line = dwg.line(id='line1', start=(295, 50), end=(95, 75), stroke='#000', stroke_width=5)
    dwg.add(line)
    line = dwg.line(id='line2', start=(400, 50), end=(300, 30), stroke='#000', stroke_width=5)
    dwg.add(line)
    dwg.save(pretty=True)
    return 0


def generate_svg(graph_votes):
    positions = nx.get_node_attributes(graph_votes, 'pos')
    coords_x = []
    coords_y = []
    for x in range(0, positions.__len__()):
        coords_x.append(positions[str(x)][0])
        coords_y.append(positions[str(x)][1])
    max_x, min_x = max(coords_x), min(coords_x)
    max_y, min_y = max(coords_y), min(coords_y)
    # print(max_x, min_x, max_y, min_y)
    radio = 0.025
    file_name = 'templates/grafo_svg.svg'
    dwg = svg.Drawing(file_name, size=('100%', '900px'),
                      viewBox='0 -0.3 1 1.4', profile='full')
    for edge in (graph_votes.edges(data=True)):
        color = select_color(int(edge[2]['duration'].split(' min')[0]))
        line = dwg.line(id='line',
                        start=((positions[edge[0]][0] - min_x) / (max_x - min_x),
                               (positions[edge[0]][1] - min_y) / (max_y - min_y)),
                        end=((positions[edge[1]][0] - min_x) / (max_x - min_x),
                             (positions[edge[1]][1] - min_y) / (max_y - min_y)),
                        stroke=color, fill=color, stroke_width=0.01)
        medio_x, medio_y = punto_medio((positions[edge[0]][0] - min_x) / (max_x - min_x),
                                       (positions[edge[0]][1] - min_y) / (max_y - min_y),
                                       (positions[edge[1]][0] - min_x) / (max_x - min_x),
                                       (positions[edge[1]][1] - min_y) / (max_y - min_y))
        time = dwg.text(edge[2]['duration'], insert=(medio_x + radio * 1.5, medio_y), stroke='none',
                        fill=color,
                        font_size=str(radio),
                        font_weight="bold",
                        font_family="Arial")
        dwg.add(time)
        dwg.add(line)
    for node in (graph_votes.nodes(data=True)):
        coord_x = (node[1]['pos'][0] - min_x) / (max_x - min_x)
        coord_y = (node[1]['pos'][1] - min_y) / (max_y - min_y)
        circle = dwg.circle(id='node' + node[0], center=(coord_x, coord_y), r=str(radio),
                            fill='black', stroke='white', stroke_width=0.010)
        dwg.add(circle)
        label = dwg.text(google_maps.reverse_geocode((node[1]['pos'][0], node[1]['pos'][1]))[0]['formatted_address'],
                         insert=(coord_x + radio * 1.5, coord_y + radio * 0.2),
                         stroke='none',
                         fill='black',
                         font_size=str(radio),
                         font_weight="bold",
                         font_family="Arial")
        dwg.add(label)
    dwg.save(pretty=True)
    return 0


def punto_medio(c_x, c_y, c_xx, c_yy):
    x = (c_x + c_xx) / 2
    y = (c_y + c_yy) / 2
    return x, y


colors = ['green', 'yellow', 'grey', 'red', 'pink', 'brown']


def select_color(time):
    if time < 2:
        color = 'green'
    elif time < 5:
        color = 'yellow'
    elif time < 8:
        color = 'grey'
    elif time < 12:
        color = 'brown'
    else:
        color = 'red'
    return color
