from xmlrpc.client import boolean
from dotenv import load_dotenv, find_dotenv
import os
from pymongo import MongoClient  # pip3 install pymongo & pip3 install "pymongo[srv]"
import certifi
import csv
from collections import defaultdict
import re


# query all single field value
def find_all_single_field_values(field_name):
    collection = gday_db.gday_info
    records = collection.find()
    values = []
    for record in records:
        if record[field_name]:
            values.append(record[field_name])
    return values


load_dotenv(find_dotenv())
MONGODB_passwd = os.environ.get("MONGODB_passwd")
connection_string = f"mongodb+srv://Wilson:{MONGODB_passwd}@cluster1.mp0is.mongodb.net/?retryWrites=true&w=majority"
# The reason use "tlsCAFile=certifi.where()", check the post from: https://www.mongodb.com/community/forums/t/serverselectiontimeouterror-ssl-certificate-verify-failed-trying-to-understand-the-origin-of-the-problem/115288
# The link for TLS/SSl and PyMongo: https://pymongo.readthedocs.io/en/stable/examples/tls.html#ocsp
# This is the Mongoose connection options: https://arunrajeevan.medium.com/understanding-mongoose-connection-options-2b6e73d96de1
# By default, poolSize is 5.
client = MongoClient(connection_string, tlsCAFile=certifi.where())
gday_db = client.gday
collection = gday_db.gday_info_1
# This is the same as collection but it has company index.
collection_2_text_index = gday_db.gday_info_2_text_index
# This is to get the members' share content.
collection_post_content = gday_db.post_content


# This is for creating the frontend tags.
def create_frontend_tags(PG_or_DB):
    langs_list = set()
    all_result_without_empty = collection.find({PG_or_DB: {"$ne": ""}})
    for langs in all_result_without_empty:
        for lang in langs[PG_or_DB]:
            langs_list.add(lang)
    return langs_list


def total_avg_salary():
    total_salary = [
        x
        for x in collection.aggregate(
            [
                {"$match": {"Salary": {"$gt": 40000, "$lte": 300000}}},
                {"$group": {"_id": "Salary", "avg Salary": {"$avg": "$Salary"}, "count number of salary": {"$sum": 1}}},
            ]
        )
    ]
    return total_salary


def get_salary_by_states():
    states_list = ["NSW", "VIC", "SA", "WA", "ACT", "QLD"]
    salary_by_states = defaultdict(list)
    for state in states_list:
        salary_by_states[state].append(
            collection.aggregate(
                [
                    {"$match": {"Office Loaction": state}},
                    {"$match": {"Salary": {"$gt": 40000, "$lte": 300000}}},
                    {"$group": {"_id": "Salary", "avg Salary": {"$avg": "$Salary"}, "count number of salary": {"$sum": 1}}},
                ]
            )
        )
    for v in salary_by_states:
        salary_by_states[v] = [i for i in salary_by_states[v][0]][0]
    return salary_by_states


def get_salary_by_range():
    great_then = 40000
    less_and_equal = 60000

    total_salary_range_one = []
    for i in range(11):
        ragne = f"{str(great_then)[:-3]}K_{str(less_and_equal)[:-3]}K"
        salary_range = collection.aggregate(
            [
                {"$match": {"Salary": {"$gt": great_then, "$lte": less_and_equal}}},
                {"$group": {"_id": "Salary", "avg Salary": {"$avg": "$Salary"}, "count number of salary": {"$sum": 1}}},
            ]
        )
        result = [count_ for count_ in salary_range][0]
        # print([count_ for count_ in salary_range][0]["count number of salary"])
        total_salary_range_one.append({ragne: round(result["avg Salary"]), "count": result["count number of salary"]})
        great_then += 20000
        less_and_equal += 20000
    return total_salary_range_one


# state="" mean all states, or give a specific state as parameter.
def sorted_langs(PG_or_DB, state=""):
    # This is to search each state
    if state:
        all_result_without_empty = collection.find({"$and": [{PG_or_DB: {"$ne": ""}}, {"Office Loaction": state}]})
    else:  # this is to search all AU
        all_result_without_empty = collection.find({PG_or_DB: {"$ne": ""}})

    # This is to distrbute the languages.
    dictionary = defaultdict(list)
    for langs in all_result_without_empty:
        for lang in langs[PG_or_DB]:
            dictionary[lang].append(1)

    # This is to sort popularity of languages.
    sorted_langs = [{i[0]: sum(i[1])} for i in sorted(dictionary.items(), key=lambda x: x[1], reverse=True)]
    return sorted_langs


def max_and_min_salary():
    max_ = collection.aggregate(
        [{"$match": {"Salary": {"$gt": 10000, "$lte": 300000}}}, {"$group": {"_id": "$Office Loaction", "max_salary": {"$max": "$Salary"}}}]
    )
    min_ = collection.aggregate(
        [{"$match": {"Salary": {"$gt": 10000, "$lte": 300000}}}, {"$group": {"_id": "$Office Loaction", "min_salary": {"$min": "$Salary"}}}]
    )

    max_list = [{i["_id"]: i["max_salary"]} for i in max_]
    min_list = [{i["_id"]: i["min_salary"]} for i in min_]
    max_min_list = {"max_list": max_list, "min_list": min_list}
    return max_min_list


def query_limit_in_hundred_docs(skipPage, company=False):

    if company:
        rgx_company = re.compile(f".*{company}.*", re.IGNORECASE)
        hundred_docs = collection_2_text_index.find({"Company Name": rgx_company}).skip(skipPage).limit(101)
    else:
        hundred_docs = collection.find({}).skip(skipPage).limit(101)
    records = []
    for value in hundred_docs:
        records.append(
            {"Company Name": value["Company Name"], "Job Title": value["Job Title"], "Office Loaction": value["Office Loaction"], "URL": value["URL"]}
        )
    return records


# =================
def insert_post_content(data):
    # Due to unique content id generated by system, so I don't need to worry about the duplication of data.
    try:
        collection_post_content.insert_one(data)
        return "OK"
    except:
        return "insert went wrong"


def query_post_content(content_id):
    try:
        share_content = collection_post_content.find({"content_id": {"$in": content_id}}, {"content_id": 1, "share_content": 1, "_id": 0})
        final_share_content = [i for i in share_content]
        return final_share_content
    except:
        return "query_post_content() went wrong"


def get_job_posts_by_state():
    try:
        job_posts = collection.aggregate([{"$group": {"_id": "$Office Loaction", "job posts by state": {"$count": {}}}}])
        job_posts_by_state = [x for x in job_posts]

        return job_posts_by_state
    except:
        return "get_job_posts_by_state() went wrong"
