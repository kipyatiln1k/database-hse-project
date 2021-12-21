from flask import Blueprint, render_template, redirect, url_for
from database.core import _create_database, _drop_database, engine, send_query
from sqlalchemy_utils import database_exists
from database.functions import FUNCTIONS_AND_PROCEDURES

app = Blueprint("home", __name__)

@app.route("/create_database")
def create_database():
    _create_database()
    return redirect(url_for('home.home'))


@app.route("/drop_database")
def drop_database():
    _drop_database()
    return redirect(url_for('home.home'))


@app.route("/clear_database")
def clear_database():
    send_query(FUNCTIONS_AND_PROCEDURES['create_database'])
    return redirect(url_for('home.home'))


@app.route("/")
def home():
    return render_template("home.html", database_exists=database_exists(engine.url))
