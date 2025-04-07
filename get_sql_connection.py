import mysql.connector

__cnx = None

def get_sql_connection():
    global __cnx
    if __cnx == None:
        __cnx = mysql.connector.connect(user='root', password='MYSQL@123',
                                      host='127.0.0.1',
                                      database = 'inventory_db')
    return __cnx

