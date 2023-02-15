import pymysql
import sys

def bbddCronTransfer():
    try:
        db = pymysql.connect(host='bbdd',user='python',password='python',database='CronTransfer',charset='utf8mb4')
        return db
    except: 
        print("Error al conectar con la base de datos")
        sys.exit(1)

# Ingresar y borrar datos

def insert_ssh(data):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO conexionssh(IP,port,user,tipo,pass,clave) VALUES (%s,%s,%s,%s,%s,%s)"
    
    try:
    # Execute the SQL command
        cursor.execute(sql,(data["HOST"],data["PORT"],data["USER"],data["TIPO"],data["PASS"],data["CLAVE"]))
    # Commit your changes in the database
        db.commit()
    except:
    # Rollback in case there is any error
        db.rollback()
        print("No se ha podido realizar el insert a causa de un error")
        sys.exit(1)


    # desconectar del servidor
    db.close()
    
def insert_share(data,borrar):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO share(origen,final,id_conexion,minutes,hours,days,months,weekday,log,sobrescribir) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    try:
    # Execute the SQL command
        cursor.execute(sql,(data["SOURCE"],data["FINAL"],data["id_conexion"],data["minutes"],data["hours"],data["days"],data["months"],data["weekday"],data["log"],data["SOBRESCRIBIR"]))
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
                delete_ssh(data["id_conexion"])
        sys.exit(1)

    # desconectar del servidor
    db.close()

def update_status(id,status):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "update share set `status`=%s where id=%s;"
    try:
        values=(status,id)
        cursor.execute(sql,values)
        db.commit()
    except:
        print("Ha fallado el borrado de la conexión, los datos que desea borrar puede ser clave foránea de otros servicios.")
        #sys.exit(1)

    db.close()        

def delete_ssh(id_ssh):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from conexionssh where id=%s;"
    try:
        cursor.execute(sql,id_ssh)
        db.commit()
    except:
        print("Ha fallado el borrado de la conexión, los datos que desea borrar puede ser clave foránea de otros servicios.")
        #sys.exit(1)

    db.close()    

def delete_share(id):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from share where id=%s;"
    try:
        cursor.execute(sql,id)
        db.commit()
    except:
        print("Ha fallado el borrado al servicio")
        sys.exit(1)

    db.close()

def delete_share_conexion(id_ssh):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "delete from share where id_conexion=%s;"
    try:
        cursor.execute(sql,id_ssh)
        db.commit()
    except:
        print("Ha fallado el borrado de los servicios")
        sys.exit(1)

    db.close()
# Consultas a la base de datos

#########################################################################
# Consultas en tabla share:
########################################################################
def select_share_id_conexion(id):
    db = bbddCronTransfer()
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
def select_share_origen_final(id):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select origen,final,sobrescribir from share where id=%s;"
    try:
        cursor.execute(sql,id)
        resultado = cursor.fetchone()
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)
    db.close()
    return(resultado)



def ultimoidSHARE():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id from share order by fecha desc;"
    try:
        cursor.execute(sql)
        resultado = cursor.fetchone()
        resultado = str(resultado[0])
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

def select_share_id_conexion(id):
    db = bbddCronTransfer()
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
def select_un_servicio(id):
    db = bbddCronTransfer()
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

def select_servicios():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select minutes, hours, days, months, weekday, log, id from share;"
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        matriz= []
        for row in datos:
            data = {
            "minutes" : row[0],
            "hours" : row[1],
            "days" : row[2],    
            "months" : row[3],
            "weekday" : row[4],
            "log": row[5],
            "id" : row[6]
            }
            matriz.append(data)       
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(matriz)


def select_status(id):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select status from share where id = %s;"
    try:
        cursor.execute(sql,id)
        datos = cursor.fetchone()
        status=datos[0]   
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(status)


#########################################################################
# Consultas en tabla conexionssh:
########################################################################


# Obtenemos el último id ofrecido 
def ultimoidssh():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select id from conexionssh order by fecha desc;"
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
def select_datos_ssh(id_ssh):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select IP, port, user,tipo, pass,clave from conexionssh where id=%s;"
    try:
        cursor.execute(sql,id_ssh)
        datosSSH = cursor.fetchone()
        data={}
        data["HOST"]= datosSSH[0]
        data["PORT"] = datosSSH[1]
        data["USER"] = datosSSH[2]
        data["TIPO"] = datosSSH[3]
        data["PASS"] = datosSSH[4]
        data["CLAVE"] = datosSSH[5]
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(data)


def select_todas_conexiones():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to select
    sql = "select id, IP, user, port, tipo, fecha from conexionssh;"

    try:
        cursor.execute(sql)
        conexiones = cursor.fetchall()

    except:
        print("Ha fallado la conexión.")
        sys.exit(1)
    db.close()
    if conexiones:
        matriz = []
        for row in conexiones:
            data = {
            "ID" : row[0],
            "IP" : row[1],
            "USER" : row[2], 
            "PORT" : row[3], 
            "TIPO": row[4],
            "FECHA": row[5]
            }
            matriz.append(data)  
        return matriz
    else:
        return 0








#########################################################################
# Consultas en varias tablas:
########################################################################

# Consulta de inner join de share y conexionssh para realizar un borrado
def select_todo():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select  sh.id, origen, final, IP, user, log, sh.id_conexion from share sh inner join conexionssh cs on sh.id_conexion=cs.id;"
    try:
        cursor.execute(sql)
        datos = cursor.fetchall() 
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)
    db.close()
    if datos:
        matriz = []
        for row in datos:
            data = {
            "ID" : row[0],
            "SOURCE": row[1], 
            "FINAL" : row[2],
            "LOG" : row[5],
            "id_conexion": row[6],
            "IP" : row[3],
            "USER" : row[4]
            }
            matriz.append(data) 
        return(matriz)
    else:
        return(0)

