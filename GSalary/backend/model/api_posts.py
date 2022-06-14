from model.database import queryOneClauseNew, insertNewMembers, queryMultileClausesNew, deleteOldrecord
from model.database_nosql import insert_post_content, query_post_content
from flask_restful import Resource
from flask import request, make_response, jsonify
import jwt  # pip3 install jwt
import os
import uuid
from dotenv import load_dotenv, find_dotenv
from collections import defaultdict

load_dotenv(find_dotenv())

# Member's post
class postsContent(Resource):
    def get(self):
        cookies = request.cookies
        if cookies:
            decoded = jwt.decode(request.cookies["access_token_cookie"], os.environ.get("SECRETKEY"), algorithms=["HS256"])

            page = request.args.get("page")
            if page is None:
                page = 0
            try:
                offsetPage = int(page) * 12
            except:
                response = make_response(jsonify({"error": True, "message": "Wrong number input"}), 400)
                return response

            member_id = decoded["sub"]["data"]["id"]
            query_posts = "SELECT * FROM posts WHERE member_id=%s order by post_id desc LIMIT 13 OFFSET %s;"
            queryResult = queryMultileClausesNew(query_posts, (member_id, offsetPage))
            if queryResult != "Wrong":
                # This is the final page.
                if len(queryResult) < 13:
                    posts = defaultdict(dict)
                    count = 1
                    NoSQL_content_id = [i[8] for i in queryResult[:12]]
                    NoSQL_result = query_post_content(NoSQL_content_id)
                    NoSQL_result.reverse()
                    for i in range(len(queryResult[:12])):
                        posts[count] = {
                            "Post Id": queryResult[:12][i][0],
                            "Company Name": queryResult[:12][i][1],
                            "Job Title": queryResult[:12][i][2],
                            "Working Hours/week": queryResult[:12][i][3],
                            "Service Year": queryResult[:12][i][4],
                            "Annual Salary": queryResult[:12][i][5],
                            "Post Time": queryResult[:12][i][6],
                            "Member Id": member_id,
                            "Post content": NoSQL_result[i]["share_content"],
                            # "page": "final_page",
                        }
                        count += 1
                    posts["nextPage"] = None
                    response = make_response(jsonify(posts), 200)
                    return response
                else:
                    posts = defaultdict(dict)
                    count = 1
                    NoSQL_content_id = [i[8] for i in queryResult[:12]]
                    NoSQL_result = query_post_content(NoSQL_content_id)
                    NoSQL_result.reverse()
                    for i in range(len(queryResult[:12])):
                        posts[count] = {
                            "Post Id": queryResult[:12][i][0],
                            "Company Name": queryResult[:12][i][1],
                            "Job Title": queryResult[:12][i][2],
                            "Working Hours/week": queryResult[:12][i][3],
                            "Service Year": queryResult[:12][i][4],
                            "Annual Salary": queryResult[:12][i][5],
                            "Post Time": queryResult[:12][i][6],
                            "Member Id": member_id,
                            "Post content": NoSQL_result[i]["share_content"],
                            # "page": "next_page",
                        }
                        count += 1
                    posts["nextPage"] = int(page) + 1
                    response = make_response(jsonify(posts), 200)
                    return response
        else:
            response = make_response(jsonify({"error": True, "message": "Internal Server Error"}), 500)
            return response

    def post(self):
        cookies = request.cookies
        content_type = request.headers.get("Content-Type")
        if content_type == "application/json" and cookies:
            decoded = jwt.decode(
                request.cookies["access_token_cookie"],
                os.environ.get("SECRETKEY"),
                algorithms=["HS256"],
            )
            jsonRequest = request.get_json()
            company_name = jsonRequest["companyNameContent"]
            job_title = jsonRequest["positionTitleContent"]
            working_hrs = jsonRequest["avghrsContent"]
            service_year = jsonRequest["serviceYearsContent"]
            salary = jsonRequest["annualSalaryContent"]
            member_id = decoded["sub"]["data"]["id"]
            randomNumber = uuid.uuid4()
            content_id = str(randomNumber)[:8] + str(member_id)

            insert = "INSERT INTO posts (company_name, position_title, avg_working_hrs, year_of_service, avg_annual_salary, member_id, content_id) VALUES(%s, %s, %s, %s, %s, %s, %s)"
            insertResult = insertNewMembers(insert, (company_name, job_title, working_hrs, service_year, salary, member_id, content_id))
            share_content = jsonRequest["textarea"]
            final_post_content = {"content_id": content_id, "share_content": share_content}

            if insertResult != "Wrong":
                insert_content_result = insert_post_content(final_post_content)
                if insert_content_result == "insert went wrong":
                    deleteOldRecord = "DELETE FROM posts WHERE content_id=%s;"
                    deleteResult = deleteOldrecord(deleteOldRecord, (content_id,))
                    response = make_response(
                        jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry, insert_post_content Nosql"}), 500
                    )
                    return response
                else:
                    response = make_response(jsonify({"post_status": "success"}), 200)
                    print("C")
                    return response
            else:
                response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry, insertResult"}), 500)
                return response
        else:
            response = make_response(jsonify({"error": True, "message": "content_type and cookie check went wrong"}), 200)
            return response


# ALL posts
class allPostsContent(Resource):
    def get(self):
        cookies = request.cookies
        if cookies:
            page = request.args.get("page")
            if page is None:
                page = 0
            try:
                offsetPage = int(page) * 12
            except:
                response = make_response(jsonify({"error": True, "message": "Wrong number input"}), 400)

            query_posts = "SELECT * FROM posts order by post_id desc LIMIT 13 OFFSET %s;"
            queryResult = queryOneClauseNew(query_posts, offsetPage)

            if queryResult != "Wrong":
                if len(queryResult) < 13:
                    posts = defaultdict(dict)
                    count = 1
                    NoSQL_content_id = [i[8] for i in queryResult[:12]]
                    NoSQL_result = query_post_content(NoSQL_content_id)
                    NoSQL_result.reverse()
                    for i in range(len(queryResult[:12])):
                        posts[count] = {
                            "Post Id": queryResult[:12][i][0],
                            "Company Name": queryResult[:12][i][1],
                            "Job Title": queryResult[:12][i][2],
                            "Working Hours/week": queryResult[:12][i][3],
                            "Service Year": queryResult[:12][i][4],
                            "Annual Salary": queryResult[:12][i][5],
                            "Post Time": queryResult[:12][i][6],
                            "Member Id": queryResult[:12][i][7],
                            "Post content": NoSQL_result[i]["share_content"],
                            # "page": "final_page",
                        }
                        count += 1
                    posts["nextPage"] = None
                    response = make_response(jsonify(posts), 200)
                    return response
                else:
                    posts = defaultdict(dict)
                    count = 1
                    NoSQL_content_id = [i[8] for i in queryResult[:12]]
                    NoSQL_result = query_post_content(NoSQL_content_id)
                    NoSQL_result.reverse()
                    for i in range(len(queryResult[:12])):
                        posts[count] = {
                            "Post Id": queryResult[:12][i][0],
                            "Company Name": queryResult[:12][i][1],
                            "Job Title": queryResult[:12][i][2],
                            "Working Hours/week": queryResult[:12][i][3],
                            "Service Year": queryResult[:12][i][4],
                            "Annual Salary": queryResult[:12][i][5],
                            "Post Time": queryResult[:12][i][6],
                            "Member Id": queryResult[:12][i][7],
                            "Post content": NoSQL_result[i]["share_content"],
                            # "page": "next_page",
                        }
                        count += 1
                    posts["nextPage"] = int(page) + 1
                    response = make_response(jsonify(posts), 200)
                    return response
        else:
            response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry"}), 500)
            return response
