"""
    metrominuto_app.calculateRoute

    FThis file contains the functions needed to extract necesary data from
    Google API.
"""
import numpy as np
from metrominuto_app import globals


def get_distance_matrix_values(matrix_distance):
    """
    Function
    :param matrix_distance: Travel distances and times for a matrix of origins and destinations
    :type matrix_distance: dict

    :return distances: Array with distances between all points.
    :rtype distances: Array
    """
    x = matrix_distance['origin_addresses'].__len__()
    y = matrix_distance['destination_addresses'].__len__()
    distances = np.zeros((x, y))
    for i in range(0, x):
        for j in range(0, y):
            distances[i, j] = matrix_distance['rows'][i]['elements'][j]['distance']['value']
    globals.global_matrix = distances
    return distances




