import numpy as np
from app import globals


def get_distance_matrix_values(matrix_distance):
    x = matrix_distance['origin_addresses'].__len__()
    y = matrix_distance['destination_addresses'].__len__()
    distances = np.zeros((x, y))
    for i in range(0, x):
        for j in range(0, y):
            distances[i, j] = matrix_distance['rows'][i]['elements'][j]['distance']['value']
    globals.global_matrix = distances
    return distances




