#-*- coding:utf-8 -*-
import pymysql
import pandas as pd
from flask import Flask

def db_connector(types, styles, abv1, abv2):
    db = pymysql.connect(host='13.209.167.99', port=3306, user='root', passwd='root', db='drinkDB', charset='utf8')
    cursor = db.cursor()
    if abv1 != abv2:
      sql = "SELECT name FROM drink_pre WHERE types=%s and styles=%s and (abv between %s and %s) limit 1;" #주류 이름 추출
      cursor.execute(sql, (types, styles, abv1, abv2))
    else: #15이상
      sql = "SELECT name FROM drink_pre WHERE types=%s and styles=%s and abv > %s limit 1;" #주류 이름 추출
      cursor.execute(sql, (types, styles, abv1))
    result = cursor.fetchall()
    db.close()
    return str(result)

