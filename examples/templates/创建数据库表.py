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
CREATE TABLE student (
Sid int(12) NOT NULL,
Sname CHAR(10) NOT NULL,
Iid int(20),
Iname CHAR(10),
Telephone CHAR(20),
Cname CHAR(20),
Cmark CHAR(20),
Class CHAR(20)
)
'''
cursor.execute(sql)
# 关闭数据库连接
db.close()
print('为数据库 mydb 创建数据表格%s:(%s)' % (sql[13:17], sql))
