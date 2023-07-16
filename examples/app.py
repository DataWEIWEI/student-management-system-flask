import json
import re

from flask import Flask, flash
from flask import render_template
from flask_bootstrap import Bootstrap
import pymysql
import traceback
from flask import request
from flask import redirect
from flask import url_for
from werkzeug.security import check_password_hash, generate_password_hash
from rich.console import Console

console = Console()
app = Flask(__name__)
app.secret_key = 'weiwei1203'
bootstrap = Bootstrap(app)


# 默认路径访问登录页面
@app.route('/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


# 获取登陆参数及处理
@app.route('/login', methods=['GET', 'POST'])
def getLoginRequset():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        if not username:
            flash('请输入用户名')
            return render_template('login.html')
        if not password:
            flash('请输入密码')
            return render_template('login.html')
        db = pymysql.connect(host="localhost", user="root", password="weiwei1203", database="studentdb")
        cursor = db.cursor()
        sql = "SELECT password FROM users WHERE username='%s'" % (username)
        cursor.execute(sql)
        results = cursor.fetchall()
        db.close()
        if len(results) == 1:
            if list(results)[0][0] == password:
                flash('欢迎{}进入网站'.format(username))
                return redirect('/student')
            else:
                flash('密码不正确不能进入系统！')
                return render_template('login.html')
        else:
            flash('用户没有注册，无法登陆！')
            return render_template('login.html')


# 获取注册请求及处理
@app.route('/regist', methods=['GET', 'POST'])
def getRegistRequest():
    if request.method == 'GET':
        return render_template('regist.html')  # get 方法直接进入 HTML 页面
    if request.method == 'POST':
        username = request.form['username']  # post 方法进行数据验证提交服务器
        password = request.form['password']
        sid = request.form['sid']
        sname = request.form['sname']
        result_password = re.compile(r'(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).{8,12}$')
        # 正则表达式：必须包含大写字母，小写字母和数字并且长度在8-12
        if not username or not password or not sid or not sname:
            flash('请输入用户名、密码、学号和姓名')
            return render_template('regist.html')
        if len(password) < 8 or len(password) > 12 or len(username) > 12:
            flash('用户名不能大于12位，密码需要8~12位，请重新设置')
            return render_template('regist.html')
        print('注册信息', username, password, sid, sname)
        db = pymysql.connect(host="localhost", user="root", password="weiwei1203", database="studentdb")
        cursor = db.cursor()
        sql = "select * from users where username='%s'" % (username)
        cursor.execute(sql)
        db.commit()
        results = cursor.fetchall()
        db.close()
        if (len(results)) >= 1:
            flash('该用户名已经注册，请重新选择！')
            return render_template('regist.html')
        if (len(results)) == 0:
            sql = "INSERT INTO users(username, password, sid, sname) VALUES ('%s', '%s', '%s', '%s')" % (username,
                                                                                                         password,
                                                                                                         sid, sname)
            cursor.execute(sql)
            db.commit()
            flash('注册成功，请直接登录！')
            return render_template('login.html')
        else:
            return render_template('regist.html')


# 访问 course 页面
@app.route('/course')
def course():
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM course"
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        return render_template('course.html', data=data)
    except:
        db.rollback()
    db.close()


@app.route('/grade')
def grade():
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM grade"
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        return render_template('grade.html', data=data)
    except:
        db.rollback()
        db.close()


# 访问 student 页面
@app.route('/student')
def student():
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT * FROM student"
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        return render_template('student.html', data=data)
    except:
        db.rollback()
    db.close()


# 添加 student 页面
@app.route('/addstudent', methods=['GET', 'POST'])
def addstudent():
    Sno = request.args.get('Sno')
    Sname = request.args.get('Sname')
    Sex = request.args.get('Sex')
    Sdept = request.args.get('Sdept')
    Csrq = request.args.get('Csrq')
    if not all([Sno, Sname, Sex, Sdept, Csrq]):
        flash('输入参数不完整！添加失败！')
        return redirect(url_for('student'))
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "INSERT INTO student(Sno, Sname, Sex, Sdept, Csrq) VALUES('%s', '%s', '%s', '%s', '%s')" % (
        Sno, Sname, Sex, Sdept, Csrq)
    try:
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('student'))
    except:
        db.rollback()
        db.close()
        return redirect(url_for('student'))


# 删除 student 函数
@app.route('/del_student/<Sno>', methods=['GET', 'POST'])
def del_student(Sno):
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "DELETE FROM student WHERE Sno='%s'" % (Sno)
    try:
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('student'))
    except:
        traceback.print_exc()
        db.rollback()
    db.close()


# 更新学生信息数据函数
@app.route('/updatedata')
def upd_std_data():
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "UPDATE student SET Sname='%s', Sex='%s', Sdept='%s', Csrq='%s' WHERE Sno='%s'" % (
        request.args.get('Sname'), request.args.get('Sex'), request.args.get('Sdept'), request.args.get('Csrq'),
        request.args.get('Sno'))
    try:
        cursor.execute(sql)
        db.commit()
        return redirect(url_for('student'))
    except:
        db.rollback()
    db.close()


# 查询学生信息函数
@app.route('/querystudent', methods=['GET', 'POST'])
def query_stu():
    query_field, query_type, query_content = request.form['query_field'], request.form['query_type'], request.form[
        'query_content']
    print(query_field, query_type, query_content)
    if not query_field or not query_type:
        return redirect(url_for("student"))
    query_type = [['=', '>', '<', 'Like'], ['=', 'Like'], ['=', 'Like'], ['=', 'Like']][int(query_field)][
        int(query_type) - 2]
    query_field = ['Sno', 'Sname', 'Sex', 'Sdept'][int(query_field)]
    print(query_field, query_type, query_content)
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    if not query_content:
        sql = "SELECT * FROM student"
    else:
        sql = "SELECT * FROM student WHERE %s %s '%s'" % (query_field, query_type, query_content)
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        data = cursor.fetchall()
        return render_template('student.html', data=data)
    except:
        db.rollback()
    db.close()


# 查询学生成绩函数
@app.route('/querysc', methods=['GET', 'POST'])
def query_sc():
    querySno, queryCno, querySdept, queryOrder = request.form['querySno'], request.form['queryCno'], request.form[
        'querySdept'], request.form['queryOrder']
    print(querySno, queryCno, querySdept, queryOrder)
    queryOrder = ['ASC', 'desc'][int(queryOrder)]
    if not querySno:
        querySno = '%%'
    if not queryCno:
        queryCno = '%%'
    if not querySdept:
        querySdept = '%%'
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT Sdept, student.Sno, Sname, Cname, Grade FROM student, sc, course WHERE student.sno = sc.sno and " \
          "course.cno = sc.cno and student.Sno like '%s' and course.cno like '%s' and Sdept like '%s' ORDER BY " \
          "Grade %s" % (querySno, queryCno, querySdept, queryOrder)
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        querydata = cursor.fetchall()
        print(querydata)
        return render_template('student.html', querydata=querydata)
    except:
        db.rollback()
    db.close()


# 显示课程成绩分布图页面函数
@app.route('/showmap/<Cname>')
def showmap(Cname):
    return render_template('showmap.html', Cname=Cname)


# 查询课程成绩分布函数
@app.route('/chartdata/<Cname>')
def chartdata(Cname):
    db = pymysql.connect(host='localHost', user='root', password='weiwei1203', db='studentdb', charset='utf8')
    cursor = db.cursor()
    sql = "SELECT Sdept, student.Sno, Sname, Cname, Grade FROM student, sc, course WHERE student.sno = sc.sno and " \
          "course.cno = sc.cno and Cname = '%s'" % (Cname)
    cursor.execute(sql)
    rest = {'title': [], 'data': []}
    state = {}
    for d in cursor.fetchall():
        if d[4] < 60:
            state['不及格'] = state.get('不及格', 0) + 1
        if 60 < d[4] < 70:
            state['及格'] = state.get('及格', 0) + 1
        if 70 <= d[4] < 80:
            state['良好'] = state.get('良好', 0) + 1
        if 80 <= d[4] <= 100:
            state['优秀'] = state.get('优秀', 0) + 1
    for grade, num in state.items():
        rest['title'].append("%s" % (grade))
        rest['data'].append({'name': "%s" % (grade), 'value': "%s" % num})
    return json.dumps(rest)
    # 通过 json 向前端传输数据


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
