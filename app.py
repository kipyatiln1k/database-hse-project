from flask import Flask

from routes.home import app as home

app = Flask(__name__, template_folder="./templates",
            static_folder="./static")

app.register_blueprint(home)


if __name__ == "__main__":
    app.run()