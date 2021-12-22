from flask import Blueprint, json, render_template, redirect, url_for, jsonify, request
from database.core import engine, send_query
from sqlalchemy_utils import database_exists
from database.functions import FUNCTIONS_AND_PROCEDURES
import json

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


@app.route("/insert_value/", methods=["POST"])
def insert_value():
    request_data_json = request.data.decode('utf-8')
    request_data = json.loads(request_data_json)
    table = request_data.pop('table')
    
    send_query(FUNCTIONS_AND_PROCEDURES[f'insert_{table}'].format(**request_data))
    
    return "ok"


@app.route("/delete_by_id/", methods=["POST"])
def delete_by_id():
    request_data_json = request.data.decode('utf-8')
    request_data = json.loads(request_data_json)

    send_query(
        FUNCTIONS_AND_PROCEDURES[f'delete_by_id'].format(**request_data))

    return "ok"


@app.route("/update_value/", methods=["POST"])
def update_value():
    request_data_json = request.data.decode('utf-8')
    request_data = json.loads(request_data_json)
    table = request_data.pop('table')
    
    send_query(
        FUNCTIONS_AND_PROCEDURES[f'update_{table}'].format(**request_data))
    
    return "ok"


@app.route("/table/<string:table_name>/get_values/")
def get_values(table_name):
    response = send_query(FUNCTIONS_AND_PROCEDURES['all_values'].format(table_name=table_name)).fetchone()[0]
    return response

@app.route("/table/<string:table_name>/")
def table(table_name):
    return render_template("table.html", table=tables[table_name])
