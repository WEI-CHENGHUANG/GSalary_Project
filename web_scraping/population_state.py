import sys

sys.path.append("..")

from fulltime_jobs_info import extract

import mysql.connector  # pip install mysql-connector-python
from mysql.connector import Error
from dotenv import load_dotenv
import os
import time

load_dotenv()


def update(update_syntax, *args):
    try:
        cursor = cnx.cursor(buffered=True)
        cursor.execute(update_syntax, *args)
        cnx.commit()
    except Error as e:
        return "Wrong"


if __name__ == "__main__":
    start = time.time()
    url = "https://www.abs.gov.au/statistics/people/population/national-state-and-territory-population/latest-release"
    soup = extract(url)

    first_table = soup.findAll("div", class_="exportable-element complex-table")[0]
    table = first_table.findChild("table")
    tbody = table.findChild("tbody")
    tr = tbody.findChildren("td")

    population_state = {}

    for i in range(len(tr)):
        if i % 4 == 0:
            population_state[tr[i].text] = ""
            # print(tr[i].text)
        elif i % 4 == 1:
            population_state[state_name] = tr[i].text
            # print(tr[i].text)
        state_name = tr[i].text
    # print(population_state)
    cnx = mysql.connector.connect(
        host=os.environ.get("host"),
        database="website",
        user="admin",
        password=os.environ.get("password"),
    )
    for key in population_state:
        name = key
        population = float(population_state[key]) * 1000
        # ==============DB==================
        update_syntax = "UPDATE populationAU SET population = %s WHERE state_name = %s"
        update(update_syntax, (population, name))
    end = time.time()
    print("4/4")
    print((end - start) / 60)
