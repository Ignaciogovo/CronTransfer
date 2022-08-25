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
        cursor.execute(sql,(data["HOST"],data["PORT"],data["USER"],data["PASS"]))
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()
        print("No se ha podido realizar el insert a causa de un error")
        sys.exit(1)


    # desconectar del servidor
    db.close()
    
def ingresarShare(data,borrar):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO share(origen,final,id_conexion,minutes,hours,days,months,weekday,log) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
    # Execute the SQL command
        cursor.execute(sql,(data["source"],data["final"],data["id_conexion"],data["minutes"],data["hours"],data["days"],data["months"],data["weekday"],data["log"]))
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()
        print("No se ha podido realizar el insert a causa de un error")
        if borrar is not None: 
            borrar=input("¿Desea borrar los datos de conexión de ssh escritos anteriormente?(Y/N)")
            if borrar== "y" or borrar == "Y":
                print("Borramos datos de conexión ssh relacionados")
                borrarSSH(data["id_conexion"])
        sys.exit(1)

    # desconectar del servidor
    db.close()

def borrarSSH(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from conexionssh where id=%s;"
    try:
        cursor.execute(sql,id)
        db.commit()
    except:
        print("Ha fallado el delete.")
        sys.exit(1)

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


def ultimoidssh():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id from conexionssh order by id desc;"
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
        resultado = str(resultado[0])
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

def ultimoidSHARE():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id from share order by id desc;"
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
        resultado = str(resultado[0])
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

def consultaridssh(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id_conexion from share where id=%s;"
    try:
        cursor.execute(sql,id)
        resultado = cursor.fetchone()
        resultado = str(resultado[0])
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)


def consultarDatosshare(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select minutes, hours, days, months, weekday, log from share where id=%s;"
    try:
        cursor.execute(sql,id)
        datos = cursor.fetchone()
        data= {
        "minutes" : datos[0],
        "hours" : datos[1],
        "days" : datos[2],    
        "months" : datos[3],
        "weekday" : datos[4],
        "id" : str(id),
        "log": datos[5]
        }
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(data)

def consultarDatosssh(id_ssh):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select IP, port, user, pass from conexionssh where id=%s;"
    try:
        cursor.execute(sql,id_ssh)
        datosSSH = cursor.fetchone()
        data={}
        data["HOST"]= datosSSH[0]
        data["PORT"] = datosSSH[1]
        data["USER"] = datosSSH[2]
        data["PASS"] = datosSSH[3]
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(data)

def consultarOrigenFinal(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select origen,final from share where id=%s;"
    try:
        cursor.execute(sql,id)
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

