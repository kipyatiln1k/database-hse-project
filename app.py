from flask import Flask
from flask_jsglue import JSGlue
from database.core import engine, _create_database, _drop_database

from routes.home import app as home
from routes.tables import app as tables


app = Flask(__name__, template_folder="./templates",
            static_folder="./static")


app.register_blueprint(home)
app.register_blueprint(tables)

jsglue = JSGlue(app)


if __name__ == "__main__":
    _drop_database()
    app.run()
