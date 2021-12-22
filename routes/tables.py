from flask import Blueprint, json, render_template, redirect, url_for, jsonify
from database.core import engine, send_query
from sqlalchemy_utils import database_exists
from database.functions import FUNCTIONS_AND_PROCEDURES

app = Blueprint("tables", __name__)


tables = {
    'city': {
        'name': 'city',
        'title': 'Города',
        'const_filename': 'js/tables/city_vars.js'
    },
    'storage': {
        'name': 'storage',
        'title': 'Cклады',
        'const_filename': 'js/tables/storage_vars.js',
    },
    'shelf': {
        'name': 'shelf',
        'title': 'Полки',
        'const_filename': 'js/tables/shelf_vars.js',
    },
    'item': {
        'name': 'item',
        'title': 'Предметы',
        'const_filename': 'js/tables/item_vars.js',
    },
    'owner': {
        'name': 'owner',
        'title': 'Владельцы',
        'const_filename': 'js/tables/owner_vars.js',
    },
}


@app.route("/table/<string:table_name>/get_values/", methods=['POST'])
def get_values(table_name):
    response = send_query(FUNCTIONS_AND_PROCEDURES['all_values'].format(table_name=table_name)).fetchone()[0]
    return response

@app.route("/table/<string:table_name>/")
def table(table_name):
    return render_template("table.html", table=tables[table_name])
