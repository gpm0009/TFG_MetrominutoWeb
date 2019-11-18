from flask import Flask, render_template, request, jsonify
#from datetime import datetime


app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def show_map():
    latitude = 42.34
    longitude = -3.69
    return render_template(
        "map_template.html",
        latitud=latitude,
        longitud=longitude
    )


@app.route("/getMarks", methods=['POST'])
def get_marks():
    markers = request.get_json();
    print(markers)
    return render_template('marks_show.html',
                           markers=markers,)


if __name__ == '__main__':
    app.run(debug=True)
