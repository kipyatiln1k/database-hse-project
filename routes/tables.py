from flask import Blueprint, render_template, redirect, url_for
from database.core import engine, send_query
from sqlalchemy_utils import database_exists
from database.functions import FUNCTIONS_AND_PROCEDURES

app = Blueprint("tables", __name__)


tables = {
    'city': {
        'name': 'Города',
    },
    'storage': {
        'name': 'Cклады',
    },
    'shelf': {
        'name': 'Полки',
    },
    'item': {
        'name': 'Предметы',
    },
    'owner': {
        'name': 'Владельцы',
    },
}


@app.route("/table/<string:table_name>/")
def table(table_name):
    return render_template("table.html", context=tables[table_name])
