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
#!/usr/bin/python
# import Config
import psycopg2
from Config1 import *

def insertevents(insert_list):
    sql = """insert into demoevents1 (eventdate,eventdays,enddate) values(%s,%s,%s)"""
    conn = None
    try:
        conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
        cur = conn.cursor()
        cur.executemany(sql,insert_list)
        conn.commit()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    insert_list = []
    d = createDates('2021-08-16',["Tuesday","Monday"],'2023-01-01')
    for i in d:
        create_row = (i,["Tuesday","Monday"],'2023-01-01',)
        insert_list.append(create_row)
    insertevents(insert_list)
    # insertevents(d,["Sunday"],'2021-08-16')
