#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

# 打开数据库连接
# 打开数据库连接
db = MySQLdb.Connect('localHost', 'root', 'weiwei1203', 'studentdb', charset='utf8')
# 使用 cursor() 方法获取操作游标
cursor = db.cursor()
# SQL 查询语句
sql = "SELECT * FROM student WHERE Iid = {}".format(4)
try:
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        Sid = row[0]
        Sname = row[1]
        Iid = row[2]
        Iname = row[3]
        Telephone = row[4]
        Cname = row[5]
        Cmark = row[6]
        Class = row[7]
        print('学生ID={},'
              '学生姓名={},'
              '学院ID={},'
              '学院名称={},'
              '联系电话={},'
              '课程名称={},'
              '课程分数={},'
              '所属班级={},'.format(Sid, Sname, Iid, Iname, Telephone, Cname, Cmark, Class))
except:
    db.rollback()
db.close()
