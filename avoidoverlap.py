from datetime import date
from datetime import datetime

init_Days = {
    "Monday" : 0,
    "Tuesday" : 1,
    "Wednesday" : 2,
    "Thursday" : 3,
    "Friday" : 4,
    "Saturday" : 5,
    "Sunday" : 6 
}
def createDates(d1,daylist,d2=None):
    initday = []
    for i in daylist:
        initday.append(init_Days[i])
    date1 = datetime.strptime(d1,'%Y-%m-%d').date()
    if(d2 is None):
        date2 = date1
        date2 = date2.replace(year = date2.year + 1)
    else:
        date2 = datetime.strptime(d2,'%Y-%m-%d').date()

    date1_ord = date1.toordinal()
    date2_ord = date2.toordinal()
    cnt = 0
    d=[]

    for d_ord in range(date1_ord,date2_ord):
        x = date.fromordinal(d_ord)
        
        if(x.weekday() in initday):
            print(x)
            d.append(x)
            cnt = cnt+1

    return d

def printdate(datelist):
    prevdate = None
    for dat in datelist:
        curdate = dat[0]
        schedule = dat[1]
        events=dat[2]
        start=dat[3]
        if(prevdate != dat[0] ):
            print(f"{curdate} --> {schedule},{events},{start}")
            prevdate = dat[0]
        else:
            print(f"-------------->{schedule},{events},{start}")

#!/usr/bin/python
# import Config
import psycopg2
from Config1 import *

def insertevents(insert_list):
    # sql1 = """CREATE EXTENSION btree_gist;"""
    sql = """insert into demo(eventdate,during,eventdays,enddate,startdate) values(%s,%s,%s,%s,%s)"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        # cur.execute(sql1)
        cur.executemany(sql,insert_list)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def altersingleduring(during2,eventdate,during1):
    sql = """update demo set during=%s where eventdate=%s and during=%s"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        # cur.execute(sql1)s
        cur.execute(sql,(during2,eventdate,during1,))
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def altersingledate(eventdate2,during,eventdate1):
    sql = """update demo set eventdate=%s where during=%s and eventdate=%s"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        # cur.execute(sql1)
        cur.execute(sql,(eventdate2,during,eventdate1,))
       
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def alterallduring(during2,during1,eventdate,_during1,_eventdate,_eventdate2,_during12):
    # sql1 = "update demo set during="+during2+ "where during="+during1+ "and startdate=(select startdate from demo where eventdate="+eventdate+" and during="+_during1+") and eventdate>="+_eventdate+" and eventdays&&(select eventdays where eventdate="+_eventdate2 +"and during="+_during12+")"
    sql = """update demo set during=%s where during=%s and startdate=(select startdate from demo where eventdate=%s and during=%s) and eventdate>=%s and eventdays&&(select eventdays from demo where eventdate=%s and during=%s)"""
    # print(sql1)
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        # cur.execute(sql1)
        cur.execute(sql,(during2,during1,eventdate,_during1,_eventdate,_eventdate2,_during12,))
       
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')            

# def alteralldays(days2,days1,eventdate,_during1,_eventdate,_eventdate2,_during12):
#     # sql1 = "update demo set during="+during2+ "where during="+during1+ "and startdate=(select startdate from demo where eventdate="+eventdate+" and during="+_during1+") and eventdate>="+_eventdate+" and eventdays&&(select eventdays where eventdate="+_eventdate2 +"and during="+_during12+")"
#     sql = """update demo set eventdays=%s where eventdays=%s and startdate=(select startdate from demo where eventdate=%s and during=%s) and eventdate>=%s and eventdays&&(select eventdays from demo where eventdate=%s and during=%s)"""
#     # print(sql1)
#     conn = None
#     try:
#         conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
#         cur = conn.cursor()
#         # cur.execute(sql1)
#         cur.execute(sql,(days2,days1,eventdate,_during1,_eventdate,_eventdate2,_during12,))
       
#         conn.commit()
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#         conn.rollback()
#     finally:
#         if conn is not None:
#             conn.close()
#             print('Database connection closed.')

def fetchData(startdate, enddate):
    sql = """ select eventdate, during, eventdays, startdate from demo where eventdate between %s and %s order by eventdate, during"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        # cur.execute(sql1)
        cur.execute(sql,(startdate, enddate,))
        result = cur.fetchall()
        printdate(result)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        conn.rollback()
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == '__main__':
    # insert_list = []
    # d = createDates('2021-09-20',["Tuesday"],'2021-12-31')
    # for i in d:
    #     create_row = (i,'[11:30,12:30]',["Tuesday"],'2021-12-31','2021-09-20')
    #     insert_list.append(create_row)
    # insertevents(insert_list)
   
    # altersingleduring('[17:30,17:45]','2021-12-14','[10:30,11:00]')
    # altersingledate('2021-09-29','[17:30,17:45]','2021-09-26')
    #   alterallduring('[17:30,17:45]','[10:00,11:00]','2021-12-14','[10:00,11:00]','2021-12-14','2021-12-14','[10:00,11:00]')
    #  fetchData('2021-08-19','2022-01-01')