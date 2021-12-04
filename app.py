from flask import Flask
import sqlalchemy
from settings import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST

from routes.home import app as home

engine = sqlalchemy.create_engine(
    f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}')

app = Flask(__name__, template_folder="./templates",
            static_folder="./static")

app.register_blueprint(home)


if __name__ == "__main__":
    app.run()
