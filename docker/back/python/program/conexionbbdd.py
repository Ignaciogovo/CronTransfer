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
    sql = "INSERT INTO conexionssh(IP,port,user,pass) VALUES (%s,%s,%s,%s)"
    
    try:
    # Execute the SQL command
        cursor.execute(sql,data.values())
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()
        print("No se ha podido realizar el insert a causa de un error")


    # desconectar del servidor
    db.close()
    
def ingresarShare(data):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO conexionssh(origen,final,id_conexion,minutes,hours,days,months,weekday,log) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    cursor.execute(sql,data["source"],data["final"],data["source"],data["id_conexion"],data["minutes"],data["hours"],data["days"],data["months"],data["weekday"],data["log"])
    try:
    # Execute the SQL command
        cursor.execute(sql)
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()
        print("No se ha podido realizar el insert a causa de un error")


    # desconectar del servidor
    db.close()


def consultarUsuario(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id_conexion from share where id=%s"
    try:
        cursor.execute(sql,id)
        resultado = cursor.fetchone()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)
    db.close()
    return(resultado)


def colsutaridssh():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id from conexionssh order by id desc;"
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

def consultartrabajos():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select * from share;"
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

