# pip3 install python-dotenv
# pip3 install mysql-connector-python
from mysql.connector import pooling, Error
from dotenv import load_dotenv
import os


# Hiding password video: https://www.youtube.com/watch?v=YdgIWTYQ69A
load_dotenv()

connection_pool = pooling.MySQLConnectionPool(
    pool_name="myWeHelpPool",
    pool_size=5,
    pool_reset_session=True,
    host=os.environ.get("host"),
    database="website",
    user="admin",
    password=os.environ.get("password"),
)

# ========================================#
# 1. Find the result, 2. return empty [], 3. return Wrong
def queryOneClauseNew(query, condition):
    try:
        oneConnection = connection_pool.get_connection()
        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(query, (condition,))
        userNameQuery = cursor.fetchall()
        return userNameQuery
    except Error as e:
        return "Wrong"
    finally:
        oneConnection.close()


# 1. Find the result, 2. return empty [], 3. return Wrong
def queryMultileClausesNew(query, *args):
    try:
        oneConnection = connection_pool.get_connection()
        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(query, *args)
        userNameQuery = cursor.fetchall()
        return userNameQuery
    except Error as e:
        return "Wrong"

    finally:
        oneConnection.close()


def queryKeyword(query, *args):
    try:
        oneConnection = connection_pool.get_connection()

        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(query, *args)
        userNameQuery = cursor.fetchall()
        return userNameQuery

    except Error as e:
        return "Wrong"

    finally:
        oneConnection.close()


def insertNewMembers(insert, *args):
    try:
        oneConnection = connection_pool.get_connection()
        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(insert, *args)
        oneConnection.commit()
    except Error as e:
        return "Wrong"

    finally:
        if oneConnection.in_transaction:
            oneConnection.rollback()
        oneConnection.close()


def deleteOldrecord(deleterecord, *args):
    try:
        oneConnection = connection_pool.get_connection()
        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(deleterecord, *args)
        oneConnection.commit()
    except Error as e:
        return "Wrong"

    finally:
        if oneConnection.in_transaction:
            oneConnection.rollback()
        oneConnection.close()


def updateRecored(insert, *args):
    try:
        oneConnection = connection_pool.get_connection()
        cursor = oneConnection.cursor(buffered=True)
        cursor.execute(insert, *args)
        oneConnection.commit()

    except Error as e:
        return "Wrong"

    finally:
        if oneConnection.in_transaction:
            oneConnection.rollback()
        oneConnection.close()
