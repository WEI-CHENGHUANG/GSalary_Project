from model.database import queryOneClauseNew
from model.database_nosql import get_job_posts_by_state
from flask_restful import Resource
from flask import request, make_response, jsonify

# count Job Posts By State
class getstateInfo(Resource):
    def get(self):
        state_full_name_dict = {
            "ACT": "Australian Capital Territory",
            "NSW": "New South Wales",
            "QLD": "Queensland",
            "VIC": "Victoria",
            "SA": "South Australia",
            "WA": "Western Australia",
        }
        state_name = request.args.get("state")
        state_full_name = state_full_name_dict[state_name]
        query_population = "SELECT population FROM populationAU WHERE state_name=%s;"
        query_result = queryOneClauseNew(query_population, (state_full_name))
        if query_result == "Wrong":
            response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry, getstateInfo(GET)"}), 500)
            return response
        if "wrong" in get_job_posts_by_state():
            response = make_response(jsonify({"error": True, "message": "Internal Server Error, we are working on it, sorry, getstateInfo(GET)"}), 500)
            return response
        else:
            for state in get_job_posts_by_state():
                if state["_id"] == state_name:
                    count_job_post = state["job posts by state"]
                    break
        return jsonify({"population": query_result[0][0], "count_job_post": count_job_post})
