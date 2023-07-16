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
INSERT INTO student(Sno, Sname, Sex, Sdept, Csrq) VALUES
(2019030780, '张三3', '男', '大数据学院', '19999996')
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
print('数据库 student 的表格%s执行插入操作(%s)!' % (sql[12:16], sql))
