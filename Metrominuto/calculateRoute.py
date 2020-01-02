from flask import Flask, render_template, request, jsonify, json
from datetime import datetime
import googlemaps


# recibe un diccionario
def read_matrix_distance(matrix_distance):
    rows = matrix_distance['rows'] #Lista de disccionarios.
    # matrix['rows'][0]['elements'][0]['distance']['value']
    for row in rows:
        elements = row['elements']
        for element in elements:
            distance = element['distance']['value']
    # matrix['destination_addresses'][0]
    destination_addresses = matrix_distance['destination_addresses'] #List
    origin_addresses = matrix_distance['origin_addresses'] #List

    return 0


# recibe una lista con un diccionario
def read_direction(directions):
    trace = directions[0] #Diccionario
    # directions_result[0]['warnings'][0]
    # directions_result[0]['waypoint_order']
    # directions_result[0]['legs'][0]['distance']['value']
    # directions_result[0]['legs'][0]['end_location']['lat']
    warnings = trace['warnings']
    for warnin in warnings:
        print(warnin)
    legs = trace['legs']
    
    return 0