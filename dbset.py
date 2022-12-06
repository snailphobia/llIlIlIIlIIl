import os
import pymysql as sql

class DB():
    ENDPOINT = 'db-key-storage.clpjvywzzlfe.eu-central-1.rds.amazonaws.com'
    PORT = 3306
    USER = 'admin'
    REGION = 'eu-central-1'
    DBNAME = 'test'
    
    def __init__(self):
        os.environ['LIBMYSQL_ENABLE_CLEARTEXT_PLUGIN'] = '1'
        self.conn = sql.connect(host=self.ENDPOINT, user=self.USER, passwd='masterslave', db = self.DBNAME, connect_timeout = 5, port=self.PORT)
        self.cursor = self.conn.cursor()
        self.cursor.execute('CREATE TABLE IF NOT EXISTS users (username VARCHAR(255), password VARCHAR(255))')
        # cursor.execute('INSERT INTO users (username, password) VALUES ("test2", "test2")')
        # cursor.execute('SELECT * FROM users LIMIT 0,10')
        # self.cursor.execute("SELECT * FROM users WHERE username = 'test'")
        # data = self.cursor.fetchall()
        # code examples because i forgot how to use sql
        # print(type(data))
        self.conn.commit()
        return

    def dbadduser(self, username, password):
        self.cursor.execute('INSERT INTO users (username, password) VALUES ("{}", "{}")'.format(username, password))
        self.conn.commit()
        return

    def dbgetuser(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username = "{}"'.format(username))
        data = self.cursor.fetchall()
        return data # returns the corresponding tuple

    def getrowforuser(self, username, context):
        self.cursor.execute('SELECT * FROM {} WHERE username = "{}"'.format(context, username))
        data = self.cursor.fetchone()
        return data # returns the tuple containing the "public" hashcode

    def end(self):
        self.conn.close()
        return
