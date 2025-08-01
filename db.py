import mysql.connector as sql


def get_connection():
    return sql.connect(
        host='sql12.freesqldatabase.com',
        user='sql12792382',
        password='5FlV4pGmQJ',
        database='sql12792382',
        port=3306
    )
def check_user(db,username):
    cur=db.cursor(dictionary=True)
    qry="SELECT * FROM credentials WHERE username=%s"
    cur.execute(qry,(username,))
    data=cur.fetchone()
    if data:
        cur.close()
        db.close()
        return data
    else:
        cur.close()
        db.close()
        return False
                
def insert_user(db,username,email,password,id):
    cur=db.cursor(dictionary=True)
    qry="INSERT INTO credentials (username, email, password, role) VALUES (%s,%s,%s,%s)"
    cur.execute(qry,(username,email,password,id))
    db.commit()
    user_id=cur.lastrowid
    cur.close()
    db.close()
    return user_id
def insert_class(db,name,teacher_id):
    cur=db.cursor()
    qry="INSERT INTO classes (NAME) VALUES (%s)"
    cur.execute(qry,(name,))
    db.commit()
    clid=cur.lastrowid
    qry2="INSERT INTO teacher_classes (teacher_id,class_id) VALUES (%s,%s)"
    cur.execute(qry2,(teacher_id,clid))
    db.commit()
    cur.close()
    db.close()
    return clid
def get_class(db,teacher_id):
    cur=db.cursor(dictionary=True)
    cur.execute("""
        SELECT c.id, c.name
        FROM teacher_classes tc
        JOIN classes c ON tc.class_id = c.id
        WHERE tc.teacher_id = %s
    """, (teacher_id,))
    classes=cur.fetchall()
    return classes
def insert_student(db,names,rolls,class_id):
    cur=db.cursor()
    for name, roll in zip(names, rolls):
        cur.execute("INSERT INTO students (name, roll_number, class_id) VALUES (%s, %s, %s)", 
                       (name, roll, class_id)) 
    db.commit()
    cur.close()
    db.close()
def get_students(db,class_id):
    cur=db.cursor(dictionary=True)
    cur.execute("SELECT id,name,roll_number FROM students WHERE class_id=%s",(class_id,))
    data=cur.fetchall()
    cur.close()
    db.close()
    return data
def markattendance(db,student_id,date,status):
    cur=db.cursor()
    cur.execute("INSERT INTO attendance (student_id,date,status) VALUES (%s,%s,%s)",(student_id,date,status))
    db.commit()
    cur.close()
    
def remove_student(db,stuid):
    cur=db.cursor()
    cur.execute("DELETE FROM attendance WHERE student_id=%s",(stuid,))
    db.commit()
    cur.execute("DELETE FROM students WHERE id=%s",(stuid,))
    db.commit()
    
def update_student(db,stuid,roll,name):

    cur = db.cursor()
    cur.execute("UPDATE students SET name=%s,roll_number=%s WHERE id=%s",(name,roll,stuid))
    db.commit()
def viewbystudent(db,stuid):
    cur =db.cursor(dictionary=True)
    cur.execute("SELECT date, status FROM attendance WHERE student_id = %s")  