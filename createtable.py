#!/usr/bin/python
# import Config
import psycopg2
from Config1 import *

def createtables():
    command = ("""
create table events(
eventdate date not null,
starttime time not null,
endtime time not null,
isrecurring boolean default False,
eventdays text[2],
enddate date	
)
""")
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error) 
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    createtables()
