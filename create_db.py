import mysql.connector

connection = mysql.connector.connect(host='localhost',port='3306',
                                     user='root',
                                     password='')

cursor = connection.cursor()

#cursor.execute("CREATE DATABASE our_users")

cursor.execute("SHOW DATABASES")

for db in cursor:
    print(db)