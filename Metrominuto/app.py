from builtins import print

from flask import Flask, render_template, request, jsonify, json
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from googlemaps import convert
from datetime import datetime
import googlemaps
import json

app = Flask(__name__)
gmaps = googlemaps.Client(key='AIzaSyBa4H59vDquLKttwMkxv0WaJrx3wXB260s')

@app.route("/", methods=['GET', 'POST'])
def show_map():
    latitude = 42.34
    longitude = -3.69
    # Se puede introducir código de places para cargar directamente el mapa donde queramos.
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude
    )

    # distance_matrix(client, origins, destinations,
    #                 mode=None, language=None, avoid=None, units=None,
    #                 departure_time=None, arrival_time=None, transit_mode=None,
    #                 transit_routing_preference=None, traffic_model=None, region=None);


@app.route("/setMarks", methods=['POST'])
def set_marks():
    place = gmaps.find_place('Burgos', 'textquery')
    print(place)

    markers = request.get_json();
    print(markers)
    origins = []
    destinations = []
    origins.append(markers[0]['position'])
    origins.append(markers[1]['position'])
    destinations.append(markers[2]['position'])
    now = datetime.now()
    # devuelven diccionarios
    origins_prueba = ["Bobcaygeon ON", [41.43206, -81.38992]]
    destinations_prueba = [(43.012486, -83.6964149),
                    {"lat": 42.8863855, "lng": -78.8781627}]

    matrix = gmaps.distance_matrix(origins_prueba, destinations_prueba)


    directions_result = gmaps.directions(markers[0]['position'],
                                         markers[1]['position'],
                                         mode="transit",
                                         departure_time=now)
    print(matrix)
    print(directions_result)
    read_matrix_distance(matrix)
    read_direction(directions_result)
    return render_template("map_template.html")


#recibe un diccionario
def read_matrix_distance(matrix_distance):
    rows = matrix_distance['rows'] #Lista de disccionarios.
    #matrix['rows'][0]['elements'][0]['distance']['value']
    for row in rows:
        elements = row['elements']
        for element in elements:
            distance = element['distance']['value']
    # matrix['destination_addresses'][0]
    destination_addresses = matrix_distance['destination_addresses'] #List
    origin_addresses = matrix_distance['origin_addresses'] #List

    return 0


#recibe una lista con un diccionario
def read_direction(directions):
    trace = directions[0] #Diccionario
    # directions_result[0]['warnings'][0]
    #directions_result[0]['waypoint_order']
    #directions_result[0]['legs'][0]['distance']['value']
    #directions_result[0]['legs'][0]['end_location']['lat']
    warnings = trace['warnings']
    for warnin in warnings:
        print(warnin)
    legs = trace['legs']
    for leg in legs:
        distance = legs['distance']['value']
        end_location_lat = leg['end_location']['lat']
        end_location_lng = leg['end_location']['lng']

    return 0

if __name__ == '__main__':
    app.run()
