# This file is to insert data to Mongodb
import csv, os
from pymongo import MongoClient
import certifi
from dotenv import load_dotenv, find_dotenv # pip install python-dotenv
import time


def check_and_create_collection(gday_db):
    collection_1 = gday_db.gday_info_1
    collection_2_text_index = gday_db.gday_info_2_text_index
    collection_name = gday_db.list_collection_names()
    if "gday_info" and "gday_info_2_text_index" in collection_name:
        collection_1.drop()
        collection_2_text_index.drop()
        create_documents(collection_1)
        create_documents(collection_2_text_index)
        collection_2_text_index.create_index("Company Name")
        print("Dropped the exist collection, and created new collection.")
        return
    create_documents(collection_1)
    create_documents(collection_2_text_index)
    collection_2_text_index.create_index("Company Name")
    print("Created new collection cuz there is no exist collection.")
    return


# convert csv data to json fromat
def create_documents(collection):
    with open("./final_result/fulltime_jobs_info.csv") as open_file:
        reader_dic = csv.DictReader(open_file)
        header = ["Job Title", "Company Name", "Office Loaction", "Salary", "PG", "DB", "URL"]
        docs = []
        for each in reader_dic:
            row = {}
            for field in header:
                if field == "Salary":
                    if each[field] != "":
                        row[field] = int(each[field])
                    else:
                        row[field] = 0
                elif field in ("PG", "DB"):
                    row[field] = each[field].split(",")
                else:
                    row[field] = each[field]
            docs.append(row)
        collection.insert_many(docs)


if __name__ == "__main__":
    start = time.time()
    load_dotenv(find_dotenv())
    MONGODB_passwd = os.environ.get("MONGODB_passwd")
    connection_string = f"mongodb+srv://Wilson:{MONGODB_passwd}@cluster1.mp0is.mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(connection_string, tlsCAFile=certifi.where())
    gday_db = client.gday
    check_and_create_collection(gday_db)
    end = time.time()
    print("3/4")
    print((end - start) / 60)