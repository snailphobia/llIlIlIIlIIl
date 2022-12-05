import os
import pymysql as sql

class DB():
    ENDPOINT='db-key-storage.clpjvywzzlfe.eu-central-1.rds.amazonaws.com'
    PORT='3306'
    USER='admin'
    REGION='eu-central-1'
    DBNAME='test'
    os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
    
    def __init__(self):
        self.conn = sql.connect(host=self.ENDPOINT, user=self.USER, passwd='masterslave', db = self.DBNAME, connect_timeout = 5)
        self.cursor = self.conn.cursor()
        # cursor.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255))')
        # cursor.execute('INSERT INTO users (username, password) VALUES ("test2", "test2")')
        # cursor.execute('SELECT * FROM users LIMIT 0,10')
        # self.cursor.execute("SELECT * FROM users WHERE username = 'test'")
        # data = self.cursor.fetchall()
        # code examples because i forgot how to use sql
        # print(type(data))
        self.conn.commit()
        self.conn.close()
        return
