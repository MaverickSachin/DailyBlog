from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    name = "Maverick"
    return render_template("index.html", name=name)
