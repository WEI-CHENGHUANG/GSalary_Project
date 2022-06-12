from crypt import methods
from flask import Flask, render_template
from flask_restful import Api
from routes import routes
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv, find_dotenv


# from flask_jwt_extended import create_access_token, set_access_cookies

load_dotenv(find_dotenv())

# Change the dir path =>https://stackoverflow.com/questions/31002890/how-to-reference-a-html-template-from-a-different-directory-in-python-flask
template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, "frontend")
template_dir = os.path.join(template_dir, "templates")

static_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
static_dir = os.path.join(static_dir, "frontend")
static_dir = os.path.join(static_dir, "static")
app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

# # ================================================
app.config["TEMPLATES_AUTO_RELOAD"] = True
# To sorted dictionary in josonify formate.
app.config["JSON_SORT_KEYS"] = False
# https://flask-jwt-extended.readthedocs.io/en/3.0.0_release/tokens_in_cookies/
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_SECRET_KEY"] = os.environ.get("SECRETKEY")

# This is to avoid CORS issue.
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
# This is for RESTful api to use.
api = Api(app)
routes(api)
jwt = JWTManager(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/state")
def state():
    return render_template("state.html")


@app.route("/memberCorner")
def memberCorner():
    return render_template("memberCorner.html")


if __name__ == "__main__":
    # app.run(port=3000, debug=True)
    app.run(host="0.0.0.0", port=3000, debug=True)
