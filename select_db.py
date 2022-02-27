import pymysql

def db_connector(types, styles, abv):
    db = pymysql.connect(host='13.209.167.99', port=3306, user='root', passwd='root', db='drinkDB', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT name FROM drink_pre WHERE types=%s and styles=%s and abv=%s limit 1;" #�ַ� �̸� ����
    cursor.execute(sql, (types, styles, abv))
    result = cursor.fetchall()
    db.close()
    return str(result)

