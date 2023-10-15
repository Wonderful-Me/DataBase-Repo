import copy
import datetime

import pandas as pd
import pymysql
from flask import Flask, redirect, render_template, request

app = Flask(__name__)



@app.route('/', methods=["GET", "POST"])
def front():
    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')

    username = request.form.get("User_Name")
    password = request.form.get("User_Password")
    print(username, password)
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from User where User_Name = %s"
    sql1 = "insert into User(User_Name, User_Password) values(%s, %s)"

    cursor.execute(sql, (username))
    data = cursor.fetchall()
    if data:
        return render_template('register.html', error="The username already exists.")

    cursor.execute(sql1, (username, password))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')

    username = request.form.get("User_Name")
    password = request.form.get("User_Password")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from User where User_Name = %s"

    cursor.execute(sql, (username))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    if not data:
        error = "The username you entered does not exist."
        return render_template('login.html', user_not_exist=error)

    if data[0]['User_Password'] == password:
        return redirect('/layout')
    else:
        error = "Wrong password."
        return render_template('login.html', wrong_pswd=error)

@app.route("/layout", methods=["GET", "POST"])
def layout():
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select * from User"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('user_list.html', data_list=data_list)

    User_Name = request.form.get("User_Name")
    print(User_Name)
    sql = "select * from User where User_Name = %s"
    print(sql)

    cursor.execute(sql, (User_Name))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('user_list.html', data_list=data_list)
 
@app.route("/publication/list", methods=["GET", "POST"])
def publication(Flag=False):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select * from Paper"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()
        if Flag == True:
            return data_list
        return render_template('publication_list.html', data_list=data_list)

    Paper_ID = request.form.get("Paper_ID")
    print(Paper_ID)
    sql = "select * from Paper where Paper_ID = %s"
    print(sql)

    cursor.execute(sql, (Paper_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('publication_list.html', data_list=data_list)

@app.route("/publication/registration", methods=["GET", "POST"])
def punlication_reg():
    if request.method == "GET":
        return render_template('publication_reg.html')

    Paper_ID = request.form.get("Paper_ID")
    Paper_name = request.form.get("Paper_name")
    Paper_src = request.form.get("Paper_src")
    address_date = request.form.get("address_date")
    Paper_type = request.form.get("Paper_type")
    level = request.form.get("level")
    Paper_name = Paper_name.replace('"', '')
    Paper_name = Paper_name.replace("'", "")
    
    Teacher_ID = request.form.get("Teacher_ID")
    Pub_Rank = request.form.get("Pub_Rank")
    coauth = request.form.get("coauth")
    
    if not Paper_ID:
        return render_template('publication_reg.html', error="Paper_ID cannot be null.")
    if not Paper_name:
        return render_template('publication_reg.html', error1="Paper_name cannot be null.")
    
    print(int(Paper_type))
    if int(Paper_type) < 1 or int(Paper_type) > 4:
        return render_template('publication_reg.html', error2="Please input legal Paper_type.")

    if int(level) < 1 or int(level) > 6:
        return render_template('publication_reg.html', error3="Please input legal Paper_level.")
    
    if not Teacher_ID or not Pub_Rank or not coauth:
        return render_template('publication_reg.html', error="Please add full information of at least one author.")    
    
    if not (coauth == "0" or coauth == "1"):
        return render_template('publication_reg.html', error4="Please input legal Is_Corresponding_Author.")    
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Paper where Paper_ID = %s"
    cursor.execute(sql, (Paper_ID))
    data = cursor.fetchall()
    if data:
        return render_template('publication_reg.html', error="The Paper_ID you entered already exist.")

    sql = "insert into Paper(Paper_ID, Paper_name, Paper_src, address_date, Paper_type, level) values(%s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (Paper_ID, Paper_name, Paper_src, address_date, Paper_type, level))
    conn.commit()

    sql = "insert into Publish(Teacher_ID, Paper_ID, Pub_Rank, coauth) values(%s, %s, %s, %s)"
    cursor.execute(sql, (Teacher_ID, Paper_ID, Pub_Rank, coauth))
    conn.commit()    
    
    cursor.close()
    conn.close()

    return redirect('/publication/registration')

@app.route("/publication/edit/<string:PID>", methods=["GET", "POST"])
def publication_edit(PID):
    if request.method == "GET":
        return render_template('publication_edit.html')
    
    Paper_ID = PID
    Paper_name = request.form.get("Paper_name")
    Paper_src = request.form.get("Paper_src")
    address_date = request.form.get("address_date")
    Paper_type = request.form.get("Paper_type")
    level = request.form.get("level")
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Paper where Paper_ID = %s"
    cursor.execute(sql, (Paper_ID))
    data = cursor.fetchall()
    
    if not Paper_name:
        Paper_name = data[0]['Paper_name']
    
    if not Paper_src:
        Paper_src = data[0]['Paper_src']
        
    if not address_date:
        address_date = data[0]['address_date']
        
    if not Paper_type:
        Paper_type = data[0]['Paper_type']
        
    if not level:
        level = data[0]['level']
        
    sql = "update Paper set Paper_name = %s, Paper_src = %s, address_date = %s, Paper_type = %s, level = %s where Paper_ID = %s"

    cursor.execute(sql, (Paper_name, Paper_src, address_date, Paper_type, level, Paper_ID))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/publication/list')

@app.route("/publication/delete/<string:PID>")
def publication_delete(PID):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "delete from Publish where Paper_ID = %s"
    cursor.execute(sql, (PID))
    conn.commit()  
    
    sql = "delete from Paper where Paper_ID = " + "'" + PID + "'"
    # sql_find = "select * from Publish where Paper_ID = %s"

    # cursor.execute(sql_find, (PID))
    # data = cursor.fetchall()

    # if data:
    #     error = "The Paper " + str(PID) + " has a publish record and is not allowed to be deleted."
    #     data_list = publication(Flag=True)
    #     return render_template('publication_list.html', data_list=data_list, error=error)

    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/publication/list')

@app.route("/publication/author", methods=["GET", "POST"])
def add_publication_info():
    if request.method == "GET":
        return render_template('publication_info_add.html')
    
    Teacher_ID = request.form.get("Teacher_ID")
    Paper_ID = request.form.get("Paper_ID")
    Pub_Rank = request.form.get("Pub_Rank")
    coauth = request.form.get("coauth")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql_1 = "select * from Teacher where Teacher_ID = %s"
    cursor.execute(sql_1, (Teacher_ID))
    data_1 = cursor.fetchall()
    
    sql_2 = "select * from Paper where Paper_ID = %s"
    cursor.execute(sql_2, (Paper_ID))
    data_2 = cursor.fetchall()

    sql_3 = "select * from Publish where Paper_ID = %s and Pub_Rank = %s"
    cursor.execute(sql_3, (Paper_ID, Pub_Rank))
    data_3 = cursor.fetchall()
    
    sql_4 = "select * from Publish where Paper_ID = %s and coauth = 1"
    cursor.execute(sql_4, (Paper_ID))
    data_4 = cursor.fetchall()
    
    sql_5 = "select * from Publish where Paper_ID = %s and Teacher_ID = %s"
    cursor.execute(sql_5, (Paper_ID, Teacher_ID))
    data_5 = cursor.fetchall()
    
    if not Teacher_ID:
        return render_template('publication_info_add.html', error="The Teacher_ID can not be null.")
    elif not Paper_ID:
        return render_template('publication_info_add.html', error="The Paper_ID can not be null.")
    elif not Pub_Rank:
        return render_template('publication_info_add.html', error="The Publication_Rank can not be null.")  
    elif not coauth:
        return render_template('publication_info_add.html', error="The Is_Corresponding_Author can not be null.")  
    
    elif not data_1:
        return render_template('publication_info_add.html', error="The Teacher_ID you entered must exist.")
    elif not data_2: 
        return render_template('publication_info_add.html', error="The Paper_ID you entered must exist.")
    
    elif data_5:
        return render_template('publication_info_add.html', error="Duplicate Author information exists.")  
    
    elif data_3:
        return render_template('publication_info_add.html', error="Duplicate rank information exists.")
    
    elif data_4 and coauth == "1":
        return render_template('publication_info_add.html', error="Corresponding Author already exists.")        
    else:
        sql = "insert into Publish(Teacher_ID , Paper_ID, Pub_Rank, coauth) values(%s, %s, %s, %s)"
        cursor.execute(sql, (Teacher_ID, Paper_ID, Pub_Rank, coauth))
        conn.commit()

    cursor.close()
    conn.close()

    return redirect('/publication/author')

@app.route("/publication/list/author/<string:PID>", methods=["GET", "POST"])
def publication_author(PID):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select Publish.Paper_ID, Paper.Paper_name, Teacher.Teacher_ID, Teacher.Teacher_name, Pub_Rank, coauth \
                from Teacher, Publish, Paper \
                where Publish.Paper_ID = %s \
                    and Publish.Paper_ID = Paper.Paper_ID \
                    and Teacher.Teacher_ID = Publish.Teacher_ID \
                order by Pub_Rank"
        cursor.execute(sql, (PID))
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('publication_author_list.html', data_list=data_list)

    Teacher_ID = request.form.get("Teacher_ID")
    print(Teacher_ID)
    sql = "select Publish.Paper_ID, Paper.Paper_name, Teacher.Teacher_ID, Teacher.Teacher_name, Pub_Rank, coauth \
                from Teacher, Publish, Paper \
                where Publish.Teacher_ID = %s \
                    and Publish.Paper_ID = Paper.Paper_ID \
                    and Teacher.Teacher_ID = Publish.Teacher_ID \
                order by Pub_Rank"
    print(sql)

    cursor.execute(sql, (Teacher_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('publication_author_list.html', data_list=data_list)

@app.route("/author/edit/<string:PID>", methods=["GET", "POST"])
def author_info_edit(PID):
    if request.method == "GET":
        return render_template('author_edit.html')
    
    Paper_ID = PID
    Teacher_ID = request.form.get("Teacher_ID")
    Pub_Rank = request.form.get("Pub_Rank")
    coauth = request.form.get("coauth")
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Publish where Paper_ID = %s"
    cursor.execute(sql, (Paper_ID))
    data = cursor.fetchall()
    
    if not Teacher_ID:
        Teacher_ID = data[0]['Teacher_ID']
    
    if not Pub_Rank:
        Pub_Rank = data[0]['Pub_Rank']
        
    if not coauth:
        coauth = data[0]['coauth']
        
    sql = "update Publish set Paper_ID = %s, Teacher_ID = %s, Pub_Rank = %s, coauth = %s"

    cursor.execute(sql, (Paper_ID, Teacher_ID, Pub_Rank, coauth))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/publication/list')

@app.route("/author/delete/<string:content>")
def author_delete(content):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    str1 = content.replace("'", "").replace(" ", "")
    str2 = str1.replace("(", "").replace(")", "")
    listi = str2.split(",")
    sql = "delete from Publish where Paper_ID = " + "'" + listi[0] + "'" + " and Teacher_ID = " + "'" + listi[1] + "'"
    print(sql)
    
    # 不能没有作者！
    # sql_find = "select * from Publish where Paper_ID = " + "'" + listi[0] + "'"
    sql_find = "select Publish.Paper_ID, Paper.Paper_name, Teacher.Teacher_ID, Teacher.Teacher_name, Pub_Rank, coauth \
                from Teacher, Publish, Paper \
                where Publish.Paper_ID = %s \
                    and Publish.Paper_ID = Paper.Paper_ID \
                    and Teacher.Teacher_ID = Publish.Teacher_ID \
                order by Pub_Rank"
    cursor.execute(sql_find, (listi[0]))
    data_list = cursor.fetchall()
    print(data_list)
    print(len(data_list))
    if len(data_list) == 1:
        return render_template('publication_author_list.html', data_list=data_list, error="The Paper must have at least one author.")
    
    print("seriously?")
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/publication/list')

ProID = 0
flag = 0

@app.route("/project/list", methods=["GET", "POST"])
def project_list(Flag=False):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select * from Project"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()
        if (Flag):
            print(data_list)
            return data_list
        return render_template('project_list.html', data_list=data_list)

    global flag
    flag = 0
    
    Project_ID = request.form.get("Project_ID")
    print(Project_ID)
    sql = "select * from Project where Project_ID = %s"
    print(sql)

    cursor.execute(sql, (Project_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('project_list.html', data_list=data_list)

@app.route("/project/registration", methods=["GET", "POST"])
def prject_reg():
    if request.method == "GET":
        return render_template('project_reg.html')

    Project_ID = request.form.get("Project_ID")
    Project_name = request.form.get("Project_name")
    Project_src = request.form.get("Project_src")
    Project_type = request.form.get("Project_type")
    funding = request.form.get("funding")
    start_year = request.form.get("start_year")
    end_year = request.form.get("end_year")

    if not Project_ID:
        return render_template('project_reg.html', error="Project_ID cannot be null.")
    if not Project_name:
        return render_template('project_reg.html', error1="Project_Name cannot be null.")
    
    if int(Project_type) < 1 or int(Project_type) > 5:
        return render_template('project_reg.html', error2="Please input legal Project_type.")
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Project where Project_ID = %s"
    cursor.execute(sql, (Project_ID))
    data = cursor.fetchall()
    if data:
        return render_template('project_reg.html', error="The Project_ID you entered already exist.")

    sql = "insert into Project(Project_ID, Project_name, Project_src, Project_type, funding, start_year, end_year) values(%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(sql, (Project_ID, Project_name, Project_src, Project_type, funding, start_year, end_year))
    conn.commit()

    cursor.close()
    conn.close()

    global ProID 
    ProID = Project_ID
    
    return redirect('/project/add_info/' + ProID)

@app.route("/project/add_info/<string:PID>", methods=["GET", "POST"])
def add_project_info(PID):
    if request.method == "GET":
        return render_template('project_info_add.html')
    
    global flag
    if flag == 0:
        global ProID
        ProID = PID
        
    Teacher_ID = request.form.get("Teacher_ID")
    Project_ID = ProID
    Pro_Rank = request.form.get("Pro_Rank")
    funding = request.form.get("funding")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql_1 = "select * from Teacher where Teacher_ID = %s"
    cursor.execute(sql_1, (Teacher_ID))
    data_1 = cursor.fetchall()
    
    sql_2 = "select * from Project where Project_ID = %s"
    cursor.execute(sql_2, (Project_ID))
    data_2 = cursor.fetchall()
    
    sql_3 = "select * from Incharge where Project_ID = %s and Pro_Rank = %s"
    cursor.execute(sql_3, (Project_ID, Pro_Rank))
    data_3 = cursor.fetchall()
    
    sql_4 = "select * from Incharge where Project_ID = %s and Teacher_ID = %s"
    cursor.execute(sql_4, (Project_ID, Teacher_ID))
    data_4 = cursor.fetchall()
    
    # funding 越界
    sql = "select funding from Incharge where Project_ID = %s"
    cursor.execute(sql, (Project_ID))
    data = cursor.fetchall()
    part = 0
    for i in range(len(data)):
        part += data[i]['funding']
    
    sql = "select funding from Project where Project_ID = %s"
    cursor.execute(sql, (Project_ID))
    data = cursor.fetchall()
    total = data[0]['funding']

    if not Teacher_ID:
        return render_template('project_info_add.html', error="The Teacher_ID can not be null.")
    elif not Project_ID:
        return render_template('project_info_add.html', error="The Project_ID can not be null.")
    elif not Pro_Rank:
        return render_template('project_info_add.html', error="The Project_Rank can not be null.")  
    elif not funding:
        return render_template('project_info_add.html', error="The funding can not be null.")  
    
    elif not data_1:
        return render_template('project_info_add.html', error="The Teacher_ID you entered must exist.")
    elif not data_2: 
        return render_template('project_info_add.html', error="The Project_ID you entered must exist.")
        
    elif data_3:
        return render_template('project_info_add.html', error="Duplicate Rank information exists.")
    
    elif data_4:
        return render_template('project_info_add.html', error="Duplicate Manager information exists.")  
    elif int(funding) + part > total:
        return render_template('project_info_add.html', error="Funding information Overflow.")  
    else:
        sql = "insert into Incharge(Teacher_ID , Project_ID, Pro_Rank, funding) values(%s, %s, %s, %s)"
        cursor.execute(sql, (Teacher_ID, Project_ID, Pro_Rank, funding))
        conn.commit()
    
    cursor.close()
    conn.close()

    if int(funding) + part == total:  
        flag = 0      
        return redirect('/project/list')
    else:        
        return redirect('/project/add_info/' + Project_ID)

@app.route("/project/list/manager/<string:PID>", methods=["GET", "POST"])
def project_manager(PID):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select Incharge.Project_ID, Project.Project_name, Teacher.Teacher_ID, Teacher.Teacher_name, Pro_Rank, Incharge.funding \
                from Teacher, Incharge, Project \
                where Incharge.Project_ID = %s \
                    and Incharge.Project_ID = Project.Project_ID \
                    and Teacher.Teacher_ID = Incharge.Teacher_ID \
                order by Pro_Rank"
        cursor.execute(sql, (PID))
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('project_manager_list.html', data_list=data_list)

    Teacher_ID = request.form.get("Teacher_ID")
    print(Teacher_ID)
    sql = "select Incharge.Project_ID, Project.Project_name, Teacher.Teacher_ID, Teacher.Teacher_name, Pro_Rank, Incharge.funding \
            from Teacher, Incharge, Project \
            where Incharge.Teacher_ID = %s \
                and Incharge.Project_ID = Project.Project_ID \
                and Teacher.Teacher_ID = Incharge.Teacher_ID \
            order by Pro_Rank"
    print(sql)

    cursor.execute(sql, (Teacher_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('project_manager_list.html', data_list=data_list)

@app.route("/manager/edit/<string:PID>", methods=["GET", "POST"])
def manager_info_edit(PID):
    if request.method == "GET":
        return render_template('manager_edit.html')
    
    Project_ID = PID
    Teacher_ID = request.form.get("Teacher_ID")
    Pro_Rank = request.form.get("Pro_Rank")
    funding = request.form.get("funding")
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Incharge where Project_ID = %s"
    cursor.execute(sql, (Project_ID))
    data = cursor.fetchall()
    
    if not Teacher_ID:
        Teacher_ID = data[0]['Teacher_ID']
    
    if not Pro_Rank:
        Pro_Rank = data[0]['Pro_Rank']
        
    if not funding:
        funding = data[0]['funding']
    
    sql = "update Incharge set Project_ID = %s, Teacher_ID = %s, Pro_Rank = %s, funding = %s"

    cursor.execute(sql, (Project_ID, Teacher_ID, Pro_Rank, funding))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/project/list')

@app.route("/manager/delete/<string:content>")
def manager_delete(content):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    str1 = content.replace("'", "").replace(" ", "")
    str2 = str1.replace("(", "").replace(")", "")
    listi = str2.split(",")
    sql = "delete from Incharge where Project_ID = " + "'" + listi[0] + "'" + " and Teacher_ID = " + "'" + listi[1] + "'"

    print(sql)
    
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/project/list')

@app.route("/project/edit/<string:PID>", methods=["GET", "POST"])
def project_edit(PID):
    if request.method == "GET":
        return render_template('project_edit.html')
    
    Project_ID = PID
    Project_name = request.form.get("Project_name")
    Project_src = request.form.get("Project_src")
    Project_type = request.form.get("Project_type")
    funding = request.form.get("funding")
    start_year = request.form.get("start_year")
    end_year = request.form.get("end_year")
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "select * from Project where Project_ID = %s"
    cursor.execute(sql, (Project_ID))
    data = cursor.fetchall()
    
    if not Project_name:
        Project_name = data[0]['Project_name']
    
    if not Project_src:
        Project_src = data[0]['Project_src']
        
    if not Project_type:
        Project_type = data[0]['Project_type']
        
    if not funding:
        funding = data[0]['funding']
        
    if not start_year:
        start_year = data[0]['start_year']
        
    if not end_year:
        end_year = data[0]['end_year']
        
    sql = "update Project set Project_name = %s, Project_src = %s, Project_type = %s, funding = %s, start_year = %s where end_year = %s"

    cursor.execute(sql, (Project_name, Project_src, Project_type, funding, start_year, end_year))
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/project/list')

@app.route("/project/delete/<string:PID>")
def project_delete(PID):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql = "delete from Incharge where Project_ID = " + "'" + PID + "'"
    cursor.execute(sql)
    conn.commit()

    sql = "delete from Project where Project_ID = " + "'" + PID + "'"
    cursor.execute(sql)
    conn.commit()

    cursor.close()
    conn.close()

    return redirect('/project/list')

@app.route("/course/list", methods=["GET", "POST"])
def course_list(Flag=False):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select * from Course"
        cursor.execute(sql)
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()
        if (Flag):
            print(data_list)
            return data_list
        return render_template('course_list.html', data_list=data_list)

    
    Course_ID = request.form.get("Course_ID")
    print(Course_ID)
    sql = "select * from Course where Course_ID = %s"
    print(sql)

    cursor.execute(sql, (Course_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('course_list.html', data_list=data_list)

@app.route("/course/list/teacher/<string:PID>", methods=["GET", "POST"])
def course_teacher(PID):
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    if request.method == "GET":
        sql = "select Teach.Course_ID, Course.Course_name, Course_hour, Course_type, Teach.Teacher_ID, Teacher.Teacher_name, year, semester, teach_hour \
                from Teacher, Teach, Course \
                where Teach.Course_ID = %s \
                    and Teach.Course_ID = Course.Course_ID \
                    and Teacher.Teacher_ID = Teach.Teacher_ID \
                order by year, semester"
        cursor.execute(sql, (PID))
        data_list = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('course_teacher_list.html', data_list=data_list)

    Teacher_ID = request.form.get("Teacher_ID")
    print(Teacher_ID)
    sql = "select Teach.Course_ID, Course.Course_name, Course_hour, Course_type, Teach.Teacher_ID, Teacher.Teacher_name, year, semester, teach_hour \
                from Teacher, Teach, Course \
                where Teach.Teacher_ID = %s \
                    and Teach.Course_ID = Course.Course_ID \
                    and Teacher.Teacher_ID = Teach.Teacher_ID \
                order by year, semester"
    print(sql)

    cursor.execute(sql, (Teacher_ID))
    data_list = cursor.fetchall()
    print(data_list)

    cursor.close()
    conn.close()

    return render_template('course_teacher_list.html', data_list=data_list)

@app.route("/course/add_info/<string:CID>", methods=["GET", "POST"])
def add_course_info(CID):
    if request.method == "GET":
        return render_template('course_info_add.html')
            
    Teacher_ID = request.form.get("Teacher_ID")
    Course_ID = CID
    Year = request.form.get("year")
    Semester = request.form.get("semester")
    Teach_Hour = request.form.get("teach_hour")

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)

    sql_1 = "select * from Teacher where Teacher_ID = %s"
    cursor.execute(sql_1, (Teacher_ID))
    data_1 = cursor.fetchall()
    
    sql_2 = "select * from Course where Course_ID = %s"
    cursor.execute(sql_2, (Course_ID))
    data_2 = cursor.fetchall()
    
    # sql_3 = "select * from Teach where Project_ID = %s and Pro_Rank = %s"
    # cursor.execute(sql_3, (Project_ID, Pro_Rank))
    # data_3 = cursor.fetchall()
    
    sql_4 = "select * from Teach where Course_ID = %s and Teacher_ID = %s and year = %s and semester = %s"
    cursor.execute(sql_4, (Course_ID, Teacher_ID, Year, Semester))
    data_4 = cursor.fetchall()
    
    # teach_hour 越界
    sql = "select teach_hour from Teach where Course_ID = %s and year = %s and semester = %s"
    cursor.execute(sql, (Course_ID, Year, Semester))
    data = cursor.fetchall()
    part = 0
    for i in range(len(data)):
        part += data[i]['teach_hour']
    
    sql = "select Course_hour from Course where Course_ID = %s"
    cursor.execute(sql, (Course_ID))
    data = cursor.fetchall()
    total = data[0]['Course_hour']

    if not Teacher_ID:
        return render_template('course_info_add.html', error="The Teacher_ID can not be null.")
    elif not Course_ID:
        return render_template('course_info_add.html', error="The Course_ID can not be null.")
    elif not Year:
        return render_template('course_info_add.html', error="The Year can not be null.")  
    elif not Semester:
        return render_template('course_info_add.html', error="The Semester can not be null.")
    elif not Teach_Hour:
        return render_template('course_info_add.html', error="The Teach_Hour can not be null.")  
    
    elif not data_1:
        return render_template('course_info_add.html', error="The Teacher_ID you entered must exist.")
    elif not data_2: 
        return render_template('course_info_add.html', error="The Course_ID you entered must exist.")
        
    # elif data_3:
    #     return render_template('course_info_add.html', error="Duplicate Rank information exists.")
    
    elif data_4:
        return render_template('course_info_add.html', error="Duplicate Teaching information exists.")  
    elif int(Semester) > 3 or int(Semester) < 1:
        return render_template('course_info_add.html', error="Please input legal Semester information.")  
    elif int(Teach_Hour) + part > total:
        return render_template('course_info_add.html', error="Funding information Overflow.")  
    else:
        sql = "insert into Teach(Teacher_ID , Course_ID, year, semester, teach_hour) values(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (Teacher_ID, Course_ID, Year, Semester, Teach_Hour))
        conn.commit()
    
    cursor.close()
    conn.close()

    if int(Teach_Hour) + part == total:  
        return redirect('/course/list')
    else:        
        return render_template('course_info_add.html', error1="Teaching Hour not enough!")  

@app.route("/teaching/edit/<string:content>", methods=["GET", "POST"])
def edit_course_info(content):
    
    if request.method == "GET":
        return render_template('course_info_add.html')
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    str1 = content.replace("'", "").replace(" ", "")
    str2 = str1.replace("(", "").replace(")", "")
    listi = str2.split(",")
    sql = "delete from Teach where Course_ID = " + "'" + listi[0] + "'" + " and Teacher_ID = " + "'" + listi[1] + "'" \
        + " and year = " + listi[2] + " and semester = " + listi[3]
    cursor.execute(sql)
    conn.commit()
    print(sql)
    
    
    Teacher_ID = request.form.get("Teacher_ID")
    print(Teacher_ID)
    Course_ID = listi[0]
    print(Course_ID)
    Year = request.form.get("year")
    Semester = request.form.get("semester")
    Teach_Hour = request.form.get("teach_hour")

    sql_1 = "select * from Teacher where Teacher_ID = %s"
    cursor.execute(sql_1, (Teacher_ID))
    data_1 = cursor.fetchall()
    
    sql_2 = "select * from Course where Course_ID = %s"
    cursor.execute(sql_2, (Course_ID))
    data_2 = cursor.fetchall()
    
    # sql_3 = "select * from Teach where Project_ID = %s and Pro_Rank = %s"
    # cursor.execute(sql_3, (Project_ID, Pro_Rank))
    # data_3 = cursor.fetchall()
    
    sql_4 = "select * from Teach where Course_ID = %s and Teacher_ID = %s and year = %s and semester = %s"
    cursor.execute(sql_4, (Course_ID, Teacher_ID, Year, Semester))
    data_4 = cursor.fetchall()
    
    # teach_hour 越界
    sql = "select teach_hour from Teach where Course_ID = %s and year = %s and semester = %s"
    cursor.execute(sql, (Course_ID, Year, Semester))
    data = cursor.fetchall()
    part = 0
    for i in range(len(data)):
        part += data[i]['teach_hour']
    
    sql = "select Course_hour from Course where Course_ID = %s"
    cursor.execute(sql, (Course_ID))
    data = cursor.fetchall()
    total = data[0]['Course_hour']

    if not Teacher_ID:
        return render_template('course_info_add.html', error="The Teacher_ID can not be null.")
    elif not Course_ID:
        return render_template('course_info_add.html', error="The Course_ID can not be null.")
    elif not Year:
        return render_template('course_info_add.html', error="The Year can not be null.")  
    elif not Semester:
        return render_template('course_info_add.html', error="The Semester can not be null.")
    elif not Teach_Hour:
        return render_template('course_info_add.html', error="The Teach_Hour can not be null.")  
    
    elif not data_1:
        return render_template('course_info_add.html', error="The Teacher_ID you entered must exist.")
    elif not data_2: 
        return render_template('course_info_add.html', error="The Course_ID you entered must exist.")
        
    # elif data_3:
    #     return render_template('course_info_add.html', error="Duplicate Rank information exists.")
    
    elif data_4:
        return render_template('course_info_add.html', error="Duplicate Teaching information exists.")  
    elif int(Semester) > 3 or int(Semester) < 1:
        return render_template('course_info_add.html', error="Please input legal Semester information.")  
    elif int(Teach_Hour) + part > total:
        return render_template('course_info_add.html', error="Funding information Overflow.")  
    else:
        sql = "insert into Teach(Teacher_ID , Course_ID, year, semester, teach_hour) values(%s, %s, %s, %s, %s)"
        cursor.execute(sql, (Teacher_ID, Course_ID, Year, Semester, Teach_Hour))
        conn.commit()
    
    cursor.close()
    conn.close()

    if int(Teach_Hour) + part == total:  
        return redirect('/course/list')
    else:        
        return render_template('course_info_add.html', error1="Teaching Hour not enough!")  
    
@app.route("/teaching/delete/<string:content>", methods=["GET", "POST"])
def delete_course_info(content):
    
    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    
    str1 = content.replace("'", "").replace(" ", "")
    str2 = str1.replace("(", "").replace(")", "")
    listi = str2.split(",")
    sql = "delete from Teach where Course_ID = " + "'" + listi[0] + "'" + " and Teacher_ID = " + "'" + listi[1] + "'" \
        + " and year = " + listi[2] + " and semester = " + listi[3]
    cursor.execute(sql)
    conn.commit()
    print(sql)
    
    cursor.close()
    conn.close()

    return redirect('/course/list')

@app.route("/about", methods=["GET", "POST"])
def author_info():

    return render_template('about.html')  

@app.route("/query", methods=["GET", "POST"])
def query():
    if request.method == "GET":
        return render_template('query_info.html')

    conn = pymysql.connect(host="127.0.0.1", port=3306, user='root', passwd='123456', db='tmsys', charset='utf8')
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)         

    Teacher_ID = request.form.get("Teacher_ID")
    Start_Year = request.form.get("Start_Year")
    End_Year = request.form.get("End_Year")
    
    sql_1 = "select * from Teacher where Teacher_ID = %s"
    cursor.execute(sql_1, (Teacher_ID))
    data_1 = cursor.fetchall()
    
    if not Teacher_ID:
        return render_template('query_info.html', error = "The Teacher_ID can not be NULL!")
    
    if not data_1:
        return render_template('query_info.html', error="The Teacher_ID you entered must exist.")
    
    if not Start_Year:
        return render_template('query_info.html', error = "The Start_Year can not be NULL!")
    
    if not End_Year:
        return render_template('query_info.html', error = "The End_Year can not be NULL!")
    
    if int(Start_Year) > int(End_Year):
        return render_template('query_info.html', error1="Start Year can not be larger than end year!")  
    
    f = open("./output/" + Teacher_ID + ".md", "w")
    f.write("# 教师教学科研工作统计 (" + Start_Year + "-" + End_Year + ")\n")



    sql = "select Teacher_ID, Teacher_name, sex, title\
        from Teacher\
            where Teacher_ID = %s"
    
    cursor.execute(sql, (Teacher_ID))
    data_list = cursor.fetchall()
    temp = data_list[0]['sex']
    if temp == 1:
        data_list[0]['sex'] = '男'
    else:
        data_list[0]['sex'] = '女'
    
    temp = data_list[0]['title']
    if temp == 1:
        data_list[0]['title'] = '博士后'
    elif temp == 2:
        data_list[0]['title'] = '助教'
    elif temp == 3:
        data_list[0]['title'] = '讲师'
    elif temp == 4:
        data_list[0]['title'] = '副教授'
    elif temp == 5:
        data_list[0]['title'] = '特任教授'
    elif temp == 6:
        data_list[0]['title'] = '教授'
    elif temp == 7:
        data_list[0]['title'] = '助理研究员'
    elif temp == 8:
        data_list[0]['title'] = '特任副研究员'
    elif temp == 9:
        data_list[0]['title'] = '副研究员'
    elif temp == 10:
        data_list[0]['title'] = '特任研究员'
    elif temp == 11:
        data_list[0]['title'] = '研究员'
    # print(data_list)
    
    teacher_Info = "## 教师基本信息\n" + \
                    "| 教师编号 | 教师姓名 | 教师性别 | 教师职称 |\n" + \
                    "| :------: | :------: | :------: | :------: |\n" + \
                    "| " + data_list[0]['Teacher_ID'] + " | " + data_list[0]['Teacher_name'] + " | " \
                    + data_list[0]['sex'] + " | " + data_list[0]['title'] + " |\n";
    f.write(teacher_Info)
    
    sql = "select Teach.Course_ID, Course.Course_name, teach_hour, year, semester \
                from Teach, Course \
                where Teach.Teacher_ID = %s \
                    and Teach.Course_ID = Course.Course_ID \
                order by year, semester"
    cursor.execute(sql, (Teacher_ID))
    data_list1 = cursor.fetchall()
    # print(data_list1)
    teach_Info = "## 教师授课信息\n" + \
        "| 课程编号 | 课程名称 | 主讲学时 | 开课年份 | 开课学期 |\n" + \
        "| :------: | :------: | :--------: | :------: | :------: |\n";
    f.write(teach_Info);

    for index, item in enumerate(data_list1):
        temp = data_list1[index]['semester']
        if temp == 1:
            data_list1[index]['semester'] = '春'
        elif temp == 2:
            data_list1[index]['semester'] = '夏'
        elif temp == 3:
            data_list1[index]['semester'] = '秋'
        info = "| " + data_list1[index]['Course_ID'] + " | " + data_list1[index]['Course_name'] + " | " + str(data_list1[index]['teach_hour']) + " | " \
                        + str(data_list1[index]['year']) + " | " +data_list1[index]['semester'] + " | \n"
        f.write(info)
        
    sql = "select Paper_name, Paper_src, address_date, level, Pub_Rank, coauth \
                from Paper, Publish \
                where Publish.Teacher_ID = %s \
                    and Publish.Paper_ID = Paper.Paper_ID"
    cursor.execute(sql, (Teacher_ID))
    data_list2 = cursor.fetchall()
    # print(data_list2)
    publish_Info = "## 教师发表论文信息 \n" + \
        "| 论文名称 | 论文来源 | 发表日期 | 论文级别 | 作者排名 | 是否为通讯作者 |\n" + \
        "| :------: | :------: | :------: | :------: | :------: | :--------------: |\n"
    f.write(publish_Info)
          
    for index, item in enumerate(data_list2):
        temp = data_list2[index]['level']
        if temp == 1:
            data_list2[index]['level'] = 'CCF-A'
        elif temp == 2:
            data_list2[index]['level'] = 'CCF-B'
        elif temp == 3:
            data_list2[index]['level'] = 'CCF-C'
        elif temp == 4:
            data_list2[index]['level'] = '中文CCF-A'
        elif temp == 5:
            data_list2[index]['level'] = '中文CCF-B'
        elif temp == 6:
            data_list2[index]['level'] = '无级别'

        temp = data_list2[index]['Pub_Rank']
        data_list2[index]['Pub_Rank'] = '排名第' + str(temp)
        
        temp = data_list2[index]['coauth']
        if temp == 1:
            data_list2[index]['coauth'] = '是' 
        else:
            data_list2[index]['coauth'] = '否';
            
        # Paper_name, Paper_src, address_date, level, Pub_Rank, coauth
        info = "| " + data_list2[index]['Paper_name'] + " | " + data_list2[index]['Paper_src'] + " | " + str(data_list2[index]['address_date']) + " | " \
                        + str(data_list2[index]['level']) + " | " + data_list2[index]['Pub_Rank'] + " | " + data_list2[index]['coauth'] + " | \n"
        f.write(info)
            
    sql = "select Project_name, Project_src, Project_type, start_year, end_year, Project.funding, Incharge.funding as Ifunding \
                from Project, Incharge \
                where Incharge.Teacher_ID = %s \
                    and Incharge.Project_ID = Project.Project_ID"
    cursor.execute(sql, (Teacher_ID))
    data_list3 = cursor.fetchall()
    # print(data_list3)
    Incharge_Info = "## 教师承担项目信息 \n" + \
                    "| 项目名称 | 项目来源 | 项目级别 | 开始时间 | 结束时间 | 总经费 | 承担经费 |\n" + \
                    "| :------: | :------: | :------: | :------: | :------: | :------: | :----------: |\n"
    f.write(Incharge_Info)
                
    for index, item in enumerate(data_list3):
        temp = data_list3[index]['Project_type']
        if temp == 1:
            data_list3[index]['Project_type'] = '国家级项目'
        elif temp == 2:
            data_list3[index]['Project_type'] = '省部级项目'
        elif temp == 3:
            data_list3[index]['Project_type'] = '市厅级项目'
        elif temp == 4:
            data_list3[index]['Project_type'] = '企业合作项目'
        elif temp == 5:
            data_list3[index]['Project_type'] = '其他项目类型'
        
        # Project_name, Project_src, Project_type, start_year, end_year, Project.funding, Incharge.funding as Ifunding \

        info = "| " + data_list3[index]['Project_name'] + " | " + data_list3[index]['Project_src'] + " | " + data_list3[index]['Project_type'] + " | " + \
                        str(data_list3[index]['start_year']) + " | " + str(data_list3[index]['end_year']) + " | " + str(data_list3[index]['funding']) + " | " + \
                            str(data_list3[index]['Ifunding']) + " |\n"
        f.write(info)
    
    cursor.close()
    conn.close()

    f.close()
    
    return render_template('query_list.html', data_list=data_list, data_list1=data_list1, data_list2=data_list2, data_list3=data_list3)
    
if __name__ == '__main__':
    app.run()