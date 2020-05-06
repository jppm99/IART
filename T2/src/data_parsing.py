import sqlite3
import pandas as pd

db = ""


def set_db_location(location):
    global db
    db = location


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_table_as_pd_dataframe(table_name):
    query = 'SELECT * FROM ' + table_name + ';'

    con = sqlite3.connect(db)
    con.row_factory = dict_factory
    cur = con.cursor()

    cur.execute(query)
    table = cur.fetchall()

    con.close()

    return pd.DataFrame(table)
