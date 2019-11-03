from flask import Flask
from flask import render_template
from datetime import datetime

app = Flask(__name__)

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello.html",
        name=name,
        date=datetime.now()
    )
