from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

db=mysql.connector.connect(
  host="localhost",
  user="root",
  password="1234",
  database="todo"
)

cur = db.cursor()
app = Flask(__name__)

#Selecting all the cards in the HOME page
@app.route('/', methods=['GET','POST'])
def index():
    cur.execute("select * from todo_list where status=0 order by id desc")
    values = cur.fetchall() 
    return render_template('index.html', values=values)

 #Inserting all the values in the HOME page   
@app.route('/insert', methods=['GET','POST'])
def insert():
    if request.method=='POST' :
        title = request.form.get('title')
        message = request.form.get('message')
        status = 0
        cur.execute("insert into todo_list(name,message,status) values (%s,%s,%s)",(title,message,status))
        db.commit()  
    return redirect(url_for('index'))

#Deleting the card when clicking the delete button
@app.route('/delete/<id>')
def delete(id):
    sql = ("delete from todo_list where id= %s")
    val = (id,)
    cur.execute(sql,val)
    db.commit()
    return redirect(url_for('index'))

#Deleting the card when clicking the delete button in complete.html
@app.route('/deletes/<id>')
def deletes(id):
    sql = ("delete from todo_list where id= %s")
    val = (id,)
    cur.execute(sql,val)
    db.commit()
    cur.execute("select * from todo_list where status=1")
    values = cur.fetchall()
    return render_template('complete.html',values=values)

#Updating the value in HOME page
@app.route('/update/<id>', methods=['GET','POST'])
def update(id):
    if request.method == 'POST' :
        mtitle = request.form.get('modaltitle')
        mmessage = request.form.get('modalmessage')
        cur.execute("update todo_list set name= %s, message= %s where id = %s", (mtitle,mmessage,id))
        db.commit()
    return redirect(url_for('index'))

#Selecting all the values whose status is 1 
@app.route('/completes')
def completes():
    cur.execute("select * from todo_list where status=1")
    values = cur.fetchall()
    return render_template('complete.html',values=values)

#Updating the status as 1 and selecting it 
@app.route('/complete/<id>', methods=['GET','POST'])
def complete(id):
    if request.method == 'POST' :
        cur.execute("update todo_list set status=1 where id = %s",(id,))
        db.commit()
        cur.execute("select * from todo_list where status=1")
        values = cur.fetchall()
    return render_template('complete.html',values=values)