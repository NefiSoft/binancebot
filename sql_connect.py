import psycopg2
from psycopg2 import sql
import json

dbname = 'd87n1rrb4jqd8'
user = 'blnwzrmviqttom'
port = '5432'
password = 'e3f54cac1b820807bba00db751e02237cf8f28d66e8914771be95211abaa44f4'
host = 'ec2-54-75-229-28.eu-west-1.compute.amazonaws.com'


def try_connect():
    try:
        conn = psycopg2.connect(dbname=dbname, user=user, port=port,
                                password=password, host=host)
        cursor = conn.cursor()
        return True
    except:
        return False


def get_json():
    conn = psycopg2.connect(dbname=dbname, user=user, port=port,
                            password=password, host=host)
    cursor = conn.cursor()
    cursor.execute('SELECT json FROM chat_info ORDER BY id DESC LIMIT 1')
    records = cursor.fetchall()
    return records
    cursor.close()
    conn.close()


def save_json(json: str):
    conn = psycopg2.connect(dbname=dbname, user=user, port=port,
                            password=password, host=host)
    with conn.cursor() as cursor:
        conn.autocommit = True
        insert = sql.SQL("INSERT INTO chat_info (json) VALUES ('" + json + "')")
        cursor.execute(insert)
        cursor.execute('''DELETE FROM chat_info
  WHERE id <= (
    SELECT id
    FROM (
      SELECT id
      FROM chat_info
      ORDER BY id DESC
      LIMIT 1 OFFSET 2 -- keep this many records
    ) foo
  )''')
        # cursor.execute('SELECT * FROM chat_info')
        # records = cursor.fetchall()
        # print(records)