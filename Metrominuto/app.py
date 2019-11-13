from flask import Flask, render_template, request
#from flask_googlemaps import GoogleMaps


from datetime import datetime

app = Flask(__name__)

@app.route("/",methods=['GET'])
def pinta_mapa():
    latitud = 42.34
    longitud = -3.69
    return render_template(
        "map_template.html",
        latitud=latitud,
        longitud=longitud
    )

@app.route("/markers")
def save_markers():
    _markers = request.args.get['markers']
    print(_markers)
    return  render_template(
        "prueba.html",
        marks=_markers,
    )

if __name__ == '__main__':
    app.run(debug=True)
