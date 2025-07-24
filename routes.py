import time
from datetime import date
from werkzeug.security import generate_password_hash,check_password_hash
import db
from flask import render_template,url_for,flash,redirect,session,request
from app import app
from app.forms import LoginForm
app.secret_key = 'kwnefm,dMM@!#$'

@app.route("/")
@app.route('/home')
@app.route('/index.html')
def home():
   if 'username' in session:
        return render_template("index.html", name=session['username'],title="Welcome!")
   else:
        return render_template("index.html",name="user",title="ATTENDANCE PORTAL")

'''

@app.route("/loading")
def loading():
   return render_template("loading.html",title="loading")
'''
@app.route('/choose_identity', methods=["GET", "POST"])
def choose_identity():
    dbs=db.get_connection()
    if request.method == "POST":
        role = request.form["role"]
        username = session.get("temp_username")
        phash = session.get("temp_password")
        remember = session.get("remember_me", False)
        email=session.get("temp_email")
        if username and phash:
            
            user_id=db.insert_user(dbs,username,email, phash, role)
            session.pop("temp_username", None)
            session.pop("temp_password", None)
            session.pop("temp_email",None)
            session["username"] = username
            session["role"] = role
            session["user_id"] = user_id
            flash("Account created and logged in!")
            return redirect(url_for("home"))
        else:
            return redirect(url_for("login"))
        return redirect(url_for("home"))

    return render_template("identity.html",title="Role")


@app.route("/login" , methods=["GET","POST"])
@app.route("/login.html" , methods=["GET","POST"])
def login():
   form=LoginForm()
   if form.validate_on_submit():
      dbs=db.get_connection()
      user=form.username.data
      pswd=form.password.data
      email=form.email.data
      check=db.check_user(dbs,user)
      if not check:
         session["temp_username"] = user
         session["temp_password"] = generate_password_hash(pswd)
         session["temp_email"] = email
         session["remember_me"] = form.remember_me.data
         return redirect(url_for("choose_identity"))
      else:
         if check_password_hash(check["password"],pswd):
            session["username"] = user
            session["user_id"] = check["id"]
            session["role"] = check["role"]
            flash("Account logged in succesfully!")
            if check['role'] == 'teacher':
                return redirect(url_for('dashboard'))
            elif check['role'] == 'student':
                return redirect(url_for('studentdashboard'))
            

   return render_template("login.html",title="Sign In",form=form)

@app.route("/logout")
def logout():
   session.clear()
   flash("You have been logged out.")
   return redirect(url_for("login"))
@app.route("/dashboard")
def dashboard():
   return render_template("dashboard.html",title="Dashboard")

@app.route("/addclass",methods=["GET","POST"])
def addclass():
   dbs=db.get_connection()
   if request.method=="POST":
      clsname=request.form["class_name"]
      t_id=session["user_id"]
      class_id=db.insert_class(dbs,clsname,t_id)
      flash("Class has been successfully added and linked to your account")
      return redirect(url_for("dashboard"))

   return render_template("addclass.html",title="create class")

@app.route("/chooseclass")
def chooseclass():
   dbs=db.get_connection()
   action=request.args.get('action')
   classes=db.get_class(dbs,session["user_id"])
   return render_template("chooseclass.html",classes=classes,action=action,title="Choose Class")
@app.route("/managestudent")
def managestudent():
   
   clsname=request.args.get("classname")
   clsid=request.args.get("class_id")
   return render_template("managestudent.html" ,classname=clsname,class_id=clsid)
@app.route("/addstudent/<int:class_id>",methods=["POST","GET"])
def addstudent(class_id):
   dbs=db.get_connection()
   names=request.form.getlist("name[]")
   rolls=request.form.getlist("roll[]")
   if names and rolls:
      db.insert_student(dbs,names,rolls,class_id)
      flash("students has been successfully added to class")
      return redirect(url_for("dashboard"))
      
   else:
      return render_template("addstudent.html",title="Add Student",class_id=class_id)
@app.route("/viewstudent/<int:class_id>/<classname>")
def viewstudent(class_id,classname):
   dbs=db.get_connection()
   students=db.get_students(dbs,class_id)
   print(students)
   if students:
      return render_template("viewstudent.html",title="students",students=students,class_id=class_id,classname=classname)
   else:
      flash("You haven't added student to this class yet")
      return redirect(url_for("dashboard"))


@app.route("/markattendance/<int:class_id>/<classname>",methods=['POST','GET'])
def markattendance(class_id,classname):
   dbs=db.get_connection()
   students=db.get_students(dbs,class_id)
   if request.method=='POST':
      
      cdate=request.form.get("date")
      if cdate:
         dbs=db.get_connection()
         for student in students:
            student_id=student["id"]
            status=request.form.get(f"status_{student_id}")
            db.markattendance(dbs,student_id,cdate,status)
         flash("Attendance marked successfully!")
         return redirect(url_for("dashboard"))
      else:
         dbs=db.get_connection()
         cdate=date.today()
         for student in students:
            student_id=student["id"]
            status=request.form.get(f"status_{student_id}")
            db.markattendance(dbs,student_id,cdate,status)
         flash("Attendance marked successfully!")
         return redirect(url_for("dashboard"))

   return render_template("markattendance.html",title="Mark Attendance",students=students,classname=classname,class_id=class_id)
   