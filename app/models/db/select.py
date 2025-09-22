import psycopg2

import app.models.db.connection as db


def select_all_from_table(table):
    query = "SELECT * FROM " + table + ";"
    try:
        conn = db.connection()
        cur = conn.cursor()
        cur.execute(query)
        result = cur.fetchall()
        conn.commit()
    except psycopg2.ProgrammingError as e:
        conn.rollback()
        print("Message systeme : ", e)
    cur.close()
    return result
