from flask_restful import Resource
from flask import request, make_response, jsonify
import os
import datetime
from flask_jwt_extended import create_access_token, set_access_cookies
from dotenv import load_dotenv, find_dotenv
from google.oauth2 import id_token  # pip3 install google-auth
from google.auth.transport import requests


load_dotenv(find_dotenv())
GOOGLE_OAUTH2_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID")


class logInByGoogle(Resource):
    def post(self):
        token = request.json["id_token"]

        try:
            id_info = id_token.verify_oauth2_token(token, requests.Request(), GOOGLE_OAUTH2_CLIENT_ID)
            if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
                raise ValueError("Wrong issuer.")
            google_id = id_info["sub"][:7]
            expires = datetime.timedelta(days=7)
            accessToken = create_access_token(
                identity={"data": {"id": google_id, "name": id_info["name"], "email": id_info["email"], "photoURL": id_info["picture"]}}, expires_delta=expires
            )
            response = make_response(jsonify({"ok": True}), 200)
            set_access_cookies(response, accessToken)
            return response
        except ValueError:
            # Invalid token
            raise ValueError("Invalid token")
