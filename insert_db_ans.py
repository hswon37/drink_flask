#-*- coding:utf-8 -*-
import pymysql 

def dbcon():
    return pymysql.connect( 
              user='root', 
              passwd='root', 
              host='13.209.167.99', 
              port=3306, 
              db='drinkDB', 
              charset='utf8' 
            )

def create_table(): 
    try: 
        db = dbcon()
        c = db.cursor() 
        c.execute("create table answer_pre ( a_id int primary key, q_id int, answer varchar(20))") 
        db.commit() 
        
    except Exception as e: 
        print('db error:', e)
         
    finally: 
        db.close()

def insert_data(q_id, answer): 
    try: 
        db = dbcon()
        c = db.cursor() 
        setdata = (q_id, answer) 
        c.execute("INSERT INTO answer_pre (q_id, answer) VALUES (%s, %s)", setdata) 
        db.commit() 
    except Exception as e: 
        print('db error:', e) 
    finally: 
        db.close()

def select_all():
    ret = list()
    try:
        db = dbcon()
        c = db.cursor()
        c.execute('SELECT * FROM answer_pre')
        ret = c.fetchall()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
        return ret

def select_answer(q_id):
    ret = ()
    try:
        db = dbcon()
        c = db.cursor()
        setdata = (q_id,)
        c.execute('SELECT answer FROM answer_pre WHERE q_id = %s order by a_id desc limit 1', setdata) #가장 최신 값만 출력하도록. 가장 최신값이 현재 응답하고 있는 사람의 응답 이라고 판단.
        ret = c.fetchone()
    except Exception as e:
        print('db error:', e)
    finally:
        db.close()
        return type(ret)