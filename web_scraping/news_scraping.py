from io import StringIO
import boto3
from bs4 import BeautifulSoup
import requests
import pandas as pd
from collections import defaultdict
from datetime import date
import mysql.connector  # pip install mysql-connector-python
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


def insert(insert_syntax, *args):
    try:
        cursor = cnx.cursor(buffered=True)
        cursor.execute(insert_syntax, *args)
        cnx.commit()
    except Error as e:
        return "Wrong"


if __name__ == "__main__":
    url = "https://www.computerworld.com/au/news/"
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"}
    scraping = requests.get(url, headers)
    soup = BeautifulSoup(scraping.content, "html.parser")
    news = soup.find_all("div", class_="index-promo")  # Two top news about IT

    cnx = mysql.connector.connect(
        host=os.environ.get("host"),
        database="website",
        user="admin",
        password=os.environ.get("password"),
    )

    for article in news:
        # scrape the news from website
        sub_content = article.find("div", class_="promo-headline").findChild("h3").findChild("a").text
        article_url = "https://www.computerworld.com" + article.findChild("a")["href"]
        image_url = article.findChild("img")["data-original"]
        today = date.today()

        # insert to RDS
        insert_syntax = "INSERT INTO news (sub_content, article_url, image_url, date) VALUES (%s, %s, %s, %s)"
        insert(insert_syntax, (sub_content, article_url, image_url, str(today)))
