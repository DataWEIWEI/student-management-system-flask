#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
# 打开数据库连接
# 打开数据库连接
db = MySQLdb.Connect('localHost', 'root', 'weiwei1203', 'studentdb', charset='utf8')
# 使用 cursor() 方法获取操作游标
cursor = db.cursor()
# SQL 删除数据语句
sql = 'DELETE FROM student WHERE Sid = {}'.format(2019030793)
try:
    cursor.execute(sql)
    db.commit()
    print('删除成功！')
except:
    db.rollback()
    print('删除失败！')
db.close()
