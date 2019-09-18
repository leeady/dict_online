"""
数据库处理操作
"""

import pymysql
import hashlib

# 对密码进行加密处理
def jm(passwd):
    salt = "^&5#Az$"
    hash = hashlib.md5(salt.encode())  # 生产加密对象
    hash.update(passwd.encode())  # 加密处理
    return hash.hexdigest()

class User:
    def __init__(self, host='localhost',
                 port = 3306,
                 user = 'root',
                 passwd = '123456',
                 charset='utf8',
                 database=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.database = database
        self.connect_db()

    # 链接数据库
    def connect_db(self):
        self.db = pymysql.connect(host = self.host,
                                  port = self.port,
                                  user=self.user,
                                  passwd=self.passwd,
                                  database=self.database,
                                  charset=self.charset)

    # 创建游标对象
    def create_cursor(self):
        self.cur = self.db.cursor()

    def register(self,name,passwd):
        sql = "select * from user where account=%s"
        self.cur.execute(sql, [name])
        r = self.cur.fetchone()
        # 查找到说明用户存在
        if r:
            return False

        # 插入用户名密码
        sql = "insert into user (account,password) \
                values (%s,%s)"
        passwd = jm(passwd) # 加密处理
        try:
            self.cur.execute(sql, [name, passwd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def login(self,name,passwd):
        sql = 'select * from user where account =%s and password =%s'
        passwd = jm(passwd)
        self.cur.execute(sql,[name,passwd])
        r = self.cur.fetchone()
        if not r:
            return False
        else:
            return True

    def query(self,word):
        sql = 'select mean from words where word=%s'
        self.cur.execute(sql,[word])
        r = self.cur.fetchone()
        if not r:
            return False
        else:
            return r[0]

    def insert_name(self,name,word):
        sql = 'insert into history (account,word) values (%s,%s)'
        try:
            self.cur.execute(sql, [name, word])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    def history(self,name):
        sql = 'select account,word,time from history where account =%s order by time desc limit 10'
        self.cur.execute(sql,[name])
        return self.cur.fetchall()


