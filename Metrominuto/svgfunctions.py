import networkx as nx
import svgwrite as svg


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
    print(max_x, min_x,max_y, min_y)
    radio = 0.025
    file_name = 'templates/grafo_svg.svg'
    dwg = svg.Drawing(file_name, size=('100%', '900px'),
                      viewBox='0 -0.3 1 1.4', profile='full')
    for edge in (graph_votes.edges(data=True)):
        line = dwg.line(id='line',
                        start=((positions[edge[0]][0]- min_x)/(max_x - min_x), (positions[edge[0]][1]- min_y)/(max_y - min_y)),
                        end=((positions[edge[1]][0]- min_x)/(max_x - min_x), (positions[edge[1]][1]- min_y)/(max_y - min_y)),
                        stroke='blue', fill='blue', stroke_width=0.01)
        medio_x, medio_y = puntoMedio((positions[edge[0]][0]- min_x)/(max_x - min_x), (positions[edge[0]][1]- min_y)/(max_y - min_y),
                                      (positions[edge[1]][0]- min_x)/(max_x - min_x), (positions[edge[1]][1]- min_y)/(max_y - min_y))
        time = dwg.text(edge[2]['duration'], insert=(medio_x+radio*1.5, medio_y),stroke='none',
                         fill='#900',
                         font_size=str(radio),
                         font_weight="bold",
                         font_family="Arial")
        dwg.add(time)
        dwg.add(line)
    for node in (graph_votes.nodes(data=True)):
        coord_x = (node[1]['pos'][0] - min_x)/(max_x - min_x)
        coord_y = (node[1]['pos'][1] - min_y)/(max_y - min_y)
        circle = dwg.circle(id='node' + node[0], center=(coord_x, coord_y), r=str(radio),
                            fill='black', stroke='white', stroke_width=0.010)
        dwg.add(circle)
        label = dwg.text("your text", insert=(coord_x+radio*1.5,coord_y+radio*0.2),stroke='none',
                         fill='#900',
                         font_size=str(radio),
                         font_weight="bold",
                         font_family="Arial")
        dwg.add(label)
    dwg.save(pretty=True)
    # reverse_geocode_result = google_maps.reverse_geocode((40.714224, -73.961452))
    # reverse_geocode_result[0]['formatted_address']
    return 0


def puntoMedio(c_x, c_y,c_xx, c_yy):
    x = (c_x + c_xx)/2
    y = (c_y+c_yy)/2
    return x, y