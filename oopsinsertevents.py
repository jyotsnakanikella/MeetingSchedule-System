from datetime import date
from datetime import datetime
from flask import app
#!/usr/bin/python
# import Config
import psycopg2
from Config1 import *
from datetime import timedelta

class Date:
    def __init__(self):
        self.init_Days = {
        "Monday" : 0,
        "Tuesday" : 1,
        "Wednesday" : 2,
        "Thursday" : 3,
        "Friday" : 4,
        "Saturday" : 5,
        "Sunday" : 6 
    }

    def changeDays(self,dateslist,eventdays1,eventdays2):
        initday = []
        # for i in daylist:
        #     initday.append(self.init_Days[i])
        if(len(eventdays1)==len(eventdays2)):
            print("came here")
            for d in dateslist:
                date1 = datetime.strptime(d,'%Y-%m-%d').date()
                for indexofe1,e1 in enumerate(eventdays1):
                    if date1.weekday() == self.init_Days[e1]:
                        print(date1)
                        date2 = date1 + timedelta(days=(self.init_Days[eventdays2[indexofe1]]-self.init_Days[e1]))
                        # date2 = date1.replace(day=date1.day+(self.init_Days[eventdays2[indexofe1]]-self.init_Days[e1]))
                        print(date2)
                        #update statement

        elif(len(eventdays1)<len(eventdays2)):
            for d in dateslist:
                date1 = datetime.strptime(d,'%Y-%m-%d').date()
                for indexofe1,e1 in enumerate(eventdays1):
                    lastindexofe1 = indexofe1
                    if date1.weekday() == self.init_Days[e1]:
                        print(date1)
                        date2 = date1 + timedelta(days=(self.init_Days[eventdays2[indexofe1]]-self.init_Days[e1]))
                        # date2 = date1.replace(day=date1.day+(self.init_Days[eventdays2[indexofe1]]-self.init_Days[e1]))
                        print(date2)
                        #update statement

                for e2 in eventdays2[lastindexofe1+1:]:
                    date2=date1+timedelta(days=(self.init_Days[e2]-date1.weekday()))
                    # date2 = date1.replace(day = date1.day+(self.init_Days[e2]-date1.weekday()))
                    #if already there in db dont add else add(might be 14 and 15 in same week will again add saturday 2 times to handle this condition)
                    print(date2)

        else:
            for d in dateslist:
                date1 = datetime.strptime(d,'%Y-%m-%d').date()
                for e1 in eventdays1:
                    if date1.weekday() == self.init_Days[e1]:
                        print(date1)
                        date2 = date1.replace(day=date1.day+(self.init_Days[eventdays2[eventdays1.index(e1)]]-self.init_Days[e1]))
                        print(date2)
                        #update statement

    def createDates(self,d1,daylist,d2=None):
        initday = []
        for i in daylist:
            initday.append(self.init_Days[i])
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

    def printdate(self,datelist):
        prevdate = None
        print(datelist)
        for dat in datelist:
            curdate = dat[0]
            print(type(dat[0]))
            schedule = dat[1]
            events=dat[2]
            start=dat[3]
            if(prevdate != dat[0] ):
                print(f"{curdate} --> {schedule},{events},{start}")
                prevdate = dat[0]
            else:
                print(f"-------------->{schedule},{events},{start}")

    def addDays(eventdateList,eventdays1,eventdays2):
        if(eventdays1.length==eventdays2.length):
            pass

class Event:

    def __init__(self):
        self.date = Date()

    def insertevents(self,insert_list):
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

    def altersingleduring(self,during2,eventdate,during1):
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

    def altersingledate(self,eventdate2,during,eventdate1):
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

    def alterallduring(self,during2,during1,eventdate,_during1,_eventdate,_eventdate2,_during12):
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

    @app.route('/recipes',methods=['GET'])
    def fetchData(self,startdate, enddate):
        user = request.args.get('user')
        print(user)
        sql = """ select eventdate, during, eventdays, startdate from demo where eventdate between %s and %s order by eventdate, during"""
        conn = None
        try:
            conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432")
            cur = conn.cursor()
            # cur.execute(sql1)
            cur.execute(sql,(startdate, enddate,))
            result = cur.fetchall()
            self.date.printdate(result)
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            conn.rollback()
        finally:
            if conn is not None:
                conn.close()
                print('Database connection closed.')

    # def alteralldays(eventdate2,eventdate1,eventdate,_during1,_eventdate,_eventdate2,_during12):
    #     sql = """update demo set during=%s where during=%s and startdate=(select startdate from demo where eventdate=%s and during=%s) and eventdate>=%s and eventdays&&(select eventdays from demo where eventdate=%s and during=%s)"""
    #     # print(sql1)
    #     conn = None
    #     try:
    #         conn = psycopg2.connect(database = "calendar", user = "postgres", password = "postgres", host = "127.0.0.1", port = "5432"
    #         cur = conn.cursor()
    #         # cur.execute(sql1)
    #         cur.execute(sql,(during2,during1,eventdate,_during1,_eventdate,_eventdate2,_during12,))
    #         conn.commit()
    #     except (Exception, psycopg2.DatabaseError) as error:
    #         print(error)
    #         conn.rollback()
    #     finally:
    #         if conn is not None:
    #             conn.close()
    #             print('Database connection closed.') 

if __name__ == '__main__':
    event = Event()
    # insert_list = []
    # d = event.date.createDates('2021-10-20',["Wednesday"],'2021-12-31')
    # for i in d:
    #     create_row = (i,'[10:30,11:30]',["Wednesday"],'2021-12-31','2021-10-20')
    #     insert_list.append(create_row)
    # event.insertevents(insert_list)
   
    # altersingleduring('[17:30,17:45]','2021-12-14','[10:30,11:00]')
    # altersingledate('2021-09-29','[17:30,17:45]','2021-09-26')
    #   alterallduring('[17:30,17:45]','[10:00,11:00]','2021-12-14','[10:00,11:00]','2021-12-14','2021-12-14','[10:00,11:00]')
    # print(type('2021-08-19'))
    # event.fetchData('2021-08-19','2022-01-01')
    event.date.changeDays(['2021-12-14','2021-12-21','2021-12-15','2021-12-22','2021-12-28','2021-12-29'],["Tuesday","Wednesday"],["Thursday","Saturday","Sunday"])