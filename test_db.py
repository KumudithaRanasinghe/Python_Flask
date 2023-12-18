from flask import Flask,render_template
import mysql.connector

connection = mysql.connector.connect(host='localhost',port='3306',
                                     database='ceylon_job_seeker',
                                     user='root',
                                     password='')

cursor = connection.cursor()

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello world!"

@app.route("/test")
def test():
    cursor.execute("SELECT * FROM jobs")
    value=cursor.fetchall()
    return render_template("test.html",data=value,name='test')


