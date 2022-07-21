import pymysql
import sys

def bbddeasybackups():
    try:
        db = pymysql.connect(host='bbdd',user='python',password='python',database='easybackups',charset='utf8mb4')
        return db
    except: 
        print("Error al conectar con la base de datos")
        sys.exit(1)


def ingresarSSH(data):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO conexionssh(IP,user,pass) VALUES (%s,%s,%s,%s)"
    cursor.execute(sql,data)
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()


    # desconectar del servidor
    db.close()
