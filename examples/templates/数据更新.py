#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

# 打开数据库连接
# 打开数据库连接
db = MySQLdb.Connect('localHost', 'root', 'weiwei1203', 'studentdb', charset='utf8')
# 使用 cursor() 方法获取操作游标
cursor = db.cursor()
# SQL 更新语句
sql = "UPDATE student SET Class = '金融工程181' WHERE Iid='{}'".format(4)
try:
    cursor.execute(sql)
    db.commit()
    print('更新成功！')
except:
    db.rollback()
    print('更新失败！')
db.close()
