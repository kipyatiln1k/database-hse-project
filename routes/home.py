from flask import Blueprint, render_template

app = Blueprint("index", __name__)


@app.route("/")
def index():
    return render_template("home.html")
