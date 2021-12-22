from flask import Blueprint, render_template, redirect, url_for
from database.core import _create_database, _drop_database, engine, send_query, count
from sqlalchemy_utils import database_exists
from database.functions import FUNCTIONS_AND_PROCEDURES
from routes.tables import tables

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
    send_query(FUNCTIONS_AND_PROCEDURES['clear_tables'])
    return redirect(url_for('home.home'))


@app.route("/test_input")
def test_input():
    for test_input in FUNCTIONS_AND_PROCEDURES['test_input']:
        send_query(test_input)
    return redirect(url_for('home.home'))


@app.route("/")
def home():
    return render_template("home.html", database_exists=database_exists(engine.url), tables=tables, count=count)
