import pymysql
import sys

def bbddeasybackups():
    try:
        db = pymysql.connect(host='bbdd',user='python',password='python',database='easybackups',charset='utf8mb4')
        return db
    except: 
        print("Error al conectar con la base de datos")
        sys.exit(1)

# Ingresar y borrar datos

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
        cursor.execute(sql,(data["SOURCE"],data["FINAL"],data["id_conexion"],data["minutes"],data["hours"],data["days"],data["months"],data["weekday"],data["log"]))
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

def borrarSSH(id_ssh):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from conexionssh where id=%s;"
    try:
        cursor.execute(sql,id_ssh)
        db.commit()
    except:
        print("Ha fallado el delete, los datos que desea borrar puede ser clave foranea de otros servicios.")
        sys.exit(1)

    db.close()    

def borrarSHARE(id):
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from share where id=%s;"
    try:
        cursor.execute(sql,id)
        db.commit()
    except:
        print("Ha fallado el delete")
        sys.exit(1)

    db.close()  
# Consultas a la base de datos

#########################################################################
# Consultas en tabla share:
########################################################################
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

# Consultamos los datos de la tabla share de forma individual
def consultar_Un_servicio(id):
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



# Consulta todos los servicios

def consultar_servicios():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select minutes, hours, days, months, weekday, log, id from share;"
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(datos)#↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        # Cuando se necesite ejecutar esta función para usamos este for para la matriz después de retornarla
        # for row in datos:
        #     data = {
        #     "minutes" : row[0],
        #     "hours" : row[1],
        #     "days" : row[2],    
        #     "months" : row[3],
        #     "weekday" : row[4],
        #     "log": row[5],
        #     "id" : row[6]
        #     }
#########################################################################
# Consultas en tabla conexionssh:
########################################################################


# Obtenemos el último id ofrecido 
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



# Consultamos los datos de conexionssh de forma individual
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


def comprobar_Conexiones():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select IP, port, user, pass, id from conexionssh;"
    try:
        cursor.execute(sql)
        datosSSH = cursor.fetchone()

    except:
        print("Ha fallado la conexión.")
        sys.exit(1)
    db.close()
    if datosSSH:
        return datosSSH
    else:
        return 0
        # for row in conexiones:
        # conexion = {
        # "IP" : row[0],
        # "PORT" : row[1],
        # "USER" : row[2],  
        # "ID" : row[3] 
        # }








#########################################################################
# Consultas en varias tablas:
########################################################################

# Consulta de inner join de share y conexionssh para realizar un borrado
def consultarParaborrados():
    db = bbddeasybackups()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select  sh.id, origen, final, IP, user,sh.id_conexion from share sh inner join conexionssh cs on sh.id_conexion=cs.id;"
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(datos)
            # Cuando se necesite ejecutar esta función para usamos este for para la matriz después de retornarla
        # for row in datos:
        #     data = {
        #     "id" : row[0],
        #     "SOURCE" : row[1],
        #     "FINAL" : row[2],    
        #     "IP" : row[3],
        #     "USER" : row[4]
        #     }


