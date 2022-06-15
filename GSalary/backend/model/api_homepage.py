from model.database_nosql import (
    get_salary_by_range,
    total_avg_salary,
    get_salary_by_states,
    create_frontend_tags,
    sorted_langs,
    max_and_min_salary,
    query_limit_in_hundred_docs,
)
from model.database import queryOneClauseNew
from flask_restful import Resource
from flask import request, make_response, jsonify
from collections import defaultdict
from datetime import date


class salary(Resource):
    def get(self):
        total_salary = defaultdict(list)
        for i in total_avg_salary():
            total_salary["avg Salary"].append(round(i["avg Salary"]))
            total_salary["count"].append(i["count number of salary"])

        salary_by_range = []
        for range_ in get_salary_by_range():
            salary_by_range.append(range_)

        salary_by_states = []
        for state in get_salary_by_states():
            salary_by_states.append(
                {state: {"avg Salary": round(get_salary_by_states()[state]["avg Salary"]), "count": get_salary_by_states()[state]["count number of salary"]}}
            )
        max_salary = max_and_min_salary()["max_list"]
        min_salary = max_and_min_salary()["min_list"]

        response_salary = make_response(
            jsonify({"total": total_salary, "by_range": salary_by_range, "by_states": salary_by_states, "max_salary": max_salary, "min_salary": min_salary})
        )

        return response_salary


class languages(Resource):
    def get(self):
        # This is to find out all languages 少ＤＢ
        lang_list = [lang for lang in create_frontend_tags("PG")]
        db_list = [lang for lang in create_frontend_tags("DB")]
        # This is for all states
        all_langs_counts = sorted_langs("PG")
        all_dbs_counts = sorted_langs("DB")
        top_five_pg = sorted_langs("PG")[:5]
        top_five_db = sorted_langs("DB")[:5]
        # The list below is to loop each state.
        states_list = ["SA", "WA", "NSW", "QLD", "ACT", "VIC"]
        all_langs_counts_by_state = defaultdict(list)
        all_dbs_counts_by_state = defaultdict(list)
        for state in states_list:
            all_langs_counts_by_state[state] = sorted_langs("PG", state)
            all_dbs_counts_by_state[state] = sorted_langs("DB", state)

        top_five_pg_by_state = [{i: all_langs_counts_by_state[i][:5]} for i in all_langs_counts_by_state]
        top_five_db_by_state = [{i: all_dbs_counts_by_state[i][:5]} for i in all_dbs_counts_by_state]
        response_language = make_response(
            jsonify(
                {
                    "lang_tags": lang_list,
                    "db_tags": db_list,
                    "total_top_five_pg": top_five_pg,
                    "total_top_five_db": top_five_db,
                    "all_langs_counts": all_langs_counts,
                    "all_dbs_counts": all_dbs_counts,
                    "all_langs_counts_by_state": all_langs_counts_by_state,
                    "all_dbs_counts_by_state": all_dbs_counts_by_state,
                    "top_five_pg_by_state": top_five_pg_by_state,
                    "top_five_db_by_state": top_five_db_by_state,
                }
            )
        )
        return response_language


class jobposts(Resource):
    def get(self):
        page = request.args.get("page")
        keyword = request.args.get("keyword")
        if page is None:
            page = 0
        try:
            skipPage = int(page) * 100
        except:
            response = make_response(jsonify({"error": True, "message": "Wrong number input"}), 400)
            return response
        # This is the last page
        if len(query_limit_in_hundred_docs(skipPage, keyword)) < 101:
            response_language = make_response(jsonify({"nextPage": None, "query_job_posts": query_limit_in_hundred_docs(skipPage, keyword)}))
        # Still having next page
        else:
            page = int(page) + 1
            response_language = make_response(jsonify({"nextPage": page, "query_job_posts": query_limit_in_hundred_docs(skipPage, keyword)[:100]}))
        return response_language


class news(Resource):
    def get(self):
        query = "SELECT sub_content, article_url, image_url, date FROM news ORDER BY id DESC LIMIT %s"
        new_detail = queryOneClauseNew(query, (2))
        response_news = make_response(jsonify({"first_news": new_detail[0], "second_news": new_detail[1]}))
        return response_news
