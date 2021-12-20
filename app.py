from flask import Flask
from database.core import engine, _create_database, _drop_database

from routes.home import app as home


app = Flask(__name__, template_folder="./templates",
            static_folder="./static")

app.register_blueprint(home)


if __name__ == "__main__":
    _drop_database()
    _create_database()
    app.run()
