from model.database import queryOneClauseNew, insertNewMembers, queryMultileClausesNew, updateRecored
from flask_restful import Resource
from flask import request, make_response, jsonify, session, Response

# pip3 install flask_jwt_extended
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
import datetime
import jwt
import os
import uuid
from werkzeug.utils import secure_filename
import boto3  # pip install boto3
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


class userIdentification(Resource):
    def get(self):
        cookies = request.cookies
        if cookies:
            decoded = jwt.decode(request.cookies["access_token_cookie"], os.environ.get("SECRETKEY"), algorithms=["HS256"])
            query_user_info = "SELECT id, name, email, photoURL FROM member WHERE email=%s;"
            member_email = decoded["sub"]["data"]["email"]
            member_name = decoded["sub"]["data"]["name"]
            member_id_from_google = decoded["sub"]["data"]["id"]
            user_info = queryOneClauseNew(query_user_info, (member_email))
            if user_info == []:
                insert = "INSERT INTO member (id, name, email, password) VALUES(%s,%s, %s, %s)"
                try:
                    insertNewMembers(insert, (member_id_from_google, member_name, member_email, "This is a google account"))
                    result = jsonify({"id": member_id_from_google, "name": member_name, "email": member_email, "photoURL": "KoalaDefault.png"})
                    return make_response(result, 200)
                except:
                    response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry"}), 500)
                    return response
            else:
                result = jsonify({"id": user_info[0][0], "name": user_info[0][1], "email": user_info[0][2], "photoURL": user_info[0][3]})
                return make_response(result, 200)
        else:
            return "null"

    def post(self):
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            jsonRequest = request.get_json()
            name = jsonRequest["name"]
            email = jsonRequest["email"]
            password = jsonRequest["password"]
            query = "SELECT name FROM member WHERE email=%s;"
            queryResult = queryOneClauseNew(query, email)
            # This is to check if the name exists or not.
            if queryResult:
                response = make_response(
                    jsonify({"error": True, "message": f"{email} already registed."}),
                    400,
                )
                return response
            else:
                insert = "INSERT INTO member (name, email, password) VALUES(%s, %s, %s)"
                try:
                    insertNewMembers(insert, (name, email, password))
                    response = make_response(jsonify({"ok": True}), 200)

                    return response
                except:
                    response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry"}), 500)
                    return response
        else:
            return "Content-Type not supported!(This info is for engineer)"

    def patch(self):
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json":
            jsonRequest = request.get_json()
            email = jsonRequest["email"]
            password = jsonRequest["password"]
            queryEmail = "SELECT email FROM member WHERE email=%s;"
            try:
                queryEmailResult = queryMultileClausesNew(queryEmail, (email,))
                if queryEmailResult:
                    try:
                        finalQuery = "SELECT id, name, email, photoURL FROM member WHERE email=%s and password=%s;"
                        finalQueryResult = queryMultileClausesNew(finalQuery, (email, password))

                        if finalQueryResult:
                            expires = datetime.timedelta(days=7)
                            accessToken = create_access_token(
                                identity={"data": {"id": finalQueryResult[0][0], "name": finalQueryResult[0][1], "email": finalQueryResult[0][2]}},
                                expires_delta=expires,
                            )
                            response = make_response(jsonify({"ok": True}), 200)
                            set_access_cookies(response, accessToken)
                            return response
                        else:
                            response = make_response(jsonify({"error": True, "message": "Wrong Password"}), 400)
                            return response
                    except:
                        response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry"}), 500)
                        return response
                else:
                    response = make_response(jsonify({"error": True, "message": "pls register this email first"}), 400)
                    return response

            except:
                response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry"}), 500)
                return response

    def delete(self):
        # Delete JWT token and clear session
        try:
            response = make_response(jsonify({"ok": True}), 200)

            g_state = request.cookies.get("g_state")
            if g_state:
                response.set_cookie(key="g_state", value="", expires=0)

            access_token_cookie = request.cookies.get("access_token_cookie")
            csrf_access_token = request.cookies.get("csrf_access_token")
            if access_token_cookie or csrf_access_token:
                response.set_cookie(key="access_token_cookie", value="", expires=0)
                response.set_cookie(key="csrf_access_token", value="", expires=0)
            return response
        except:
            return " Delect JWT went Wrong => userIdentification(delete)"


class memberInfo(Resource):
    def post(self):
        decoded = jwt.decode(
            request.cookies["access_token_cookie"],
            os.environ.get("SECRETKEY"),
            algorithms=["HS256"],
        )
        member_email = decoded["sub"]["data"]["email"]
        # upload photo to S3
        s3 = boto3.client(
            "s3",
            aws_access_key_id=os.environ.get("aws_access_key_id"),
            aws_secret_access_key=os.environ.get("aws_secret_access_key"),
            region_name=os.environ.get("region_name"),
        )
        image = request.files["file"]
        if image:
            content_type = request.mimetype
            image.filename = str(uuid.uuid4())
            filename = secure_filename(image.filename)
        # update the photo url name in MySQL
        url = f"https://d19u9n2870afb4.cloudfront.net/{filename}"
        update_url = "UPDATE member SET photoURL = %s WHERE email = %s"
        updated_result = updateRecored(update_url, (filename, member_email))
        if updated_result == "Wrong":
            response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry."}), 500)
            return response
        else:
            s3.put_object(Body=image, Bucket="bootcamp-assignment", Key=filename, ContentType=content_type)
            response = jsonify({"file_name": filename, "URL": url})
            return response
