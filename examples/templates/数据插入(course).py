#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb

# 打开数据库连接
# 打开数据库连接
db = MySQLdb.Connect('localhost', 'root', 'weiwei1203', 'studentdb', charset='utf8')
# 使用 cursor() 方法获取操作游标
cursor = db.cursor()
# SQL 插入语句
sql = '''
INSERT INTO course(Cno, Cname, Cpno, Ccredit) VALUES
('1', '数据库', '0', 2.1),
('2', '数据库1', '0', 2.1),
('3', '数据库2', '0', 2.1)
'''
try:
    cursor.execute(sql)
    db.commit()
    print('插入成功！')
except:
    db.rollback()
    print('插入失败！')
# 关闭数据库连接
db.close()
print('数据库 course 的表格%s执行插入操作(%s)!' % (sql[12:16], sql))
