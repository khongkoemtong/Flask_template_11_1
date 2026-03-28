from flask import Flask,render_template,request,url_for,redirect
import pymysql
import os

import uuid

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER



def conect_db():
    conection = pymysql.connect(
        host='localhost',
        user='root',
        passwd='',
        db='testing'
    )
    if (not conection ):
        print("can not connect to database ! 🥲🥲")
    print("Connect to database success !🎉🥳")    

    return conection
conect_db()


@app.route('/update',methods=['POST'])
def update():
    conection = conect_db()
    cursor = conection.cursor()
    
    id = request.form['update_id']
    name = request.form['update_username']
    age = request.form['update_age']
    gender = request.form['update_gender']
    salary = request.form['update_salary']


    sql = "UPDATE users SET Name = %s,Age = %s,Gender = %s , Salary = %s Where id = %s"

    cursor.execute(sql,(name,age,gender,salary,id))
    conection.commit()

    return redirect(url_for('homepage'))


@app.route('/')
def homepage ():
    conection = conect_db()
    cursor = conection.cursor()

    cursor.execute('SELECT * FROM users')
    user = cursor.fetchall()

    return render_template('home.html',user=user)


@app.route('/insert' ,methods=['POST'])
def insert():
    conection = conect_db()
    cursor = conection.cursor()

    username = request.form['username']
    age = request.form['age']
    gender = request.form['gender']
    salary = request.form['salary']

    file = request.files['image']

    if file :
        pus_image = os.path.splitext(file.filename)[1]
        filename = str(uuid.uuid4())+pus_image
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
    

        
        

    sql = "INSERT INTO users (Name,Age,Gender,Salary,image) Values (%s,%s,%s,%s,%s)"
    cursor.execute(sql,(username,age,gender,salary,filename))
    conection.commit()

    return redirect(url_for('homepage'))


@app.route('/delete' ,methods=['POST'])
def delete():
    conection = conect_db()
    cursor = conection.cursor()

    id = request.form['id']

    sql = "DELETE FROM users WHERE id =%s"
    cursor.execute(sql,(id))
    conection.commit()

    return redirect(url_for('homepage'))









if __name__=="__main__":
    app.run(debug=True)