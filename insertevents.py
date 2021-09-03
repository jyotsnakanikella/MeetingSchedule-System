#!/usr/bin/python
# import Config
import psycopg2
from Config1 import *

def insertevents(eventdate, starttime, endtime, isrecurring,eventdays,enddate):
    sql = """insert into events(eventdate,starttime,endtime,isrecurring,eventdays,enddate) values(%s,%s,%s,%s,%s,%s)"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        cur.execute(sql,(eventdate, starttime, endtime, isrecurring,eventdays,enddate,))
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    insertevents('2021-08-15','16:45','17:45',True,["Sunday"],'2021-08-16')
