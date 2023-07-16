#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

# 打开数据库连接
db = MySQLdb.Connect('localHost', 'root', 'weiwei1203', 'studentdb', charset='utf8')
# 使用 cursor() 方法获取操作游标
cursor = db.cursor()
# 如果数据表已经存在使用 execute() 方法删除表
cursor.execute('DROP TABLE IF EXISTS STUDENT')
# 创建数据表 SQL 语句
sql = '''
CREATE TABLE users (
UId int(12) primary key auto_increment,
Username CHAR(12) NOT NUll UNIQUE,
Password CHAR(255) NOT NULL,
Sid CHAR(12) NOT NULL,
Sname CHAR(12) NOT NULL
)
'''
cursor.execute(sql)
db.close()
print('为数据库 student 创建数据表格{}：{}'.format(sql[13:17], sql))
