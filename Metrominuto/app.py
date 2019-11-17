from flask import Flask, render_template, request
#from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=['GET'])
def pinta_mapa():
    latitude = 42.34
    longitude = -3.69
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude
    )


def save_markers():
    print("save markers")
    return 0


if __name__ == '__main__':
    app.run(debug=True)
