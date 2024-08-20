from flask import Flask, redirect, url_for, request, render_template
import sqlite3


login_teacher =  {"Ad Kon": "AK12345", "Bin Jane": "BJ12345"}
login_student = {"Victor Non": "VN123", "Grace Joe": "GJ123"}

def teacher_info(name):
  result = []
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT *
  FROM Teacher
  WHERE name = (?)
  """,(name,))
  result = cursor.fetchall()
  conn.commit()
  conn.close()

  return result

def teacher_add_annc(post_date, to_group, about, priority, due_date):
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  INSERT INTO Teacher_Annc(post_date, to_group, about, priority, due_date)
  VALUES(?,?,?,?,?)
  ;
  """,(post_date, to_group, about, priority, due_date))
  
  conn.commit()
  conn.close()

def teacher_read_annc(to_group):
  result = []
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT *
  FROM Teacher_Annc
  WHERE to_group = (?);
  """,(to_group,))

  result = cursor.fetchall()
  
  conn.commit()
  conn.close()

  return result

def student_info(name):
  result = []
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT *
  FROM Student
  WHERE name = (?)
  """,(name,))
  result = cursor.fetchall()
  conn.commit()
  conn.close()
  
  return result

def student_find_class(cm_name):
  result = ""
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT cm
  FROM Teacher
  WHERE name = (?)
  """,(cm_name,))
  result = cursor.fetchone()
  conn.commit()
  conn.close()
  
  return result

def student_find_subject(cm_name):
  result = ""
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT subject
  FROM Teacher
  WHERE name = (?)
  """,(cm_name,))
  result = cursor.fetchone()
  conn.commit()
  conn.close()
  
  return result

def student_read_info(from_group):
  result = []
  conn = sqlite3.connect("school.db")
  cursor = conn.cursor()

  cursor.execute("""
  SELECT *
  FROM Teacher_Annc
  WHERE to_group = (?);
  """,(from_group,))

  result = cursor.fetchall()
  
  conn.commit()
  conn.close()

  return result

app = Flask(__name__)

@app.route('/')
def index():
  btn = request.args.get("Login")
  username = request.args.get("username")
  password = request.args.get("password")

  if username in login_teacher:
    if password == login_teacher[username]:
      return redirect(url_for("teacher",usr=username))

  if username in login_student:
    if password == login_student[username]:
      return redirect(url_for("student",usr=username))
    
  return render_template("index.html")


@app.route('/teacher/<usr>')
def teacher(usr):
  post_date = request.args.get("post_date")
  to_group = request.args.get("to_group")
  about = request.args.get("about")
  priority = request.args.get("priority")
  due_date = request.args.get("due_date")

  teacher_add_annc(post_date, to_group, about, priority, due_date)
  result = teacher_info(usr)
  
  cm_table = teacher_read_annc(result[0][1])
  subject_table = teacher_read_annc(result[0][2])
  cca_table = teacher_read_annc(result[0][3])
  
  
  return render_template("teacher.html",name=result[0][0],cm=result[0][1],cg=result[0][2],cca=result[0][3],subject=result[0][4], cm_table = cm_table, subject_table=subject_table, cca_table=cca_table)


@app.route('/student/<usr>')
def student(usr):
  result = student_info(usr)
  cm_table = teacher_read_annc(student_find_class(result[0][1])[0])
  cm_table = [list(x) for x in cm_table]
  for i in range(len(cm_table)):
    if usr == "Victor Non":
      cm_table[i][1] = "Bin Jane"
    else:
      cm_table[i][1] = "Ad Kon"

  if usr == "Victor Non":
    subject_table = teacher_read_annc('25/06')
  else:
    subject_table = teacher_read_annc('25/20')
    
  subject_table = [list(x) for x in subject_table]

  for i in range(len(subject_table)):
    if usr == "Victor Non":
      subject_table[i][1] = "Ad Kon"
    else:
      subject_table[i][1] = "Bin Jane"
  
  cca_table = student_read_info(result[0][3])
  return render_template("student.html",name=result[0][0],cm=result[0][1], cg=student_find_class(result[0][1])[0],subject=result[0][2],cca=result[0][3], cm_table = cm_table,subject_table=subject_table,cca_table = cca_table)
# cm_table=cm_table,subject_table=subject_table,

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)
