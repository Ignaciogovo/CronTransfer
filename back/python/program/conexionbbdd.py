import pymysql
import sys
import os

user_db = os.getenv("MYSQL_USER")
password_db = os.getenv("MYSQL_PASSWORD")
def bbddCronTransfer():
    try:
        db = pymysql.connect(host='bbdd',user=user_db,password=password_db,database='CronTransfer',charset='utf8mb4')
        return db
    except: 
        print("Error al conectar con la base de datos")
        sys.exit(1)

# Ingresar y borrar datos

def ingresarSSH(data):
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
    
def ingresarShare(data,borrar):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "INSERT INTO share(origen,final,id_conexion,crontab,log,sobrescribir) VALUES (%s,%s,%s,%s,%s,%s)"
    try:
    # Execute the SQL command
        cursor.execute(sql,(data["SOURCE"],data["FINAL"],data["id_conexion"],data["crontab"],data["log"],data["SOBRESCRIBIR"]))
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




def borrarSSH(id_ssh):
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

def borrarSHARE(id):
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

def borrarSHARE_conexion(id_ssh):
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
def consultarUsuario(id):
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
def consultarOrigenFinal(id):
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
        if resultado:
            resultado = str(resultado[0])
        else:
            resultado = str(0)
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(resultado)

def consultaridssh(id):
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
def consultar_Un_servicio(id):
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select crontab, log, status from share where id=%s;"
    try:
        cursor.execute(sql,id)
        datos = cursor.fetchone()
        data= {
        "crontab" : datos[0],
        "id" : str(id),
        "log": datos[1]
        }
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(data)



# Consulta todos los servicios

def consultar_servicios():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select crontab, log, id from share;"
    try:
        cursor.execute(sql)
        datos = cursor.fetchall()
        matriz= []
        for row in datos:
            data = {
            "crontab" : row[0],
            "log" : row[1],
            "id" : row[2]
            }
            matriz.append(data)       
    except:
        print("Ha fallado la conexión.")
        sys.exit(1)

    db.close()
    return(matriz)

def consultar_status(id):
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
def consultarDatosssh(id_ssh):
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


def comprobar_Conexiones():
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
def consultar_Servicio():
    db = bbddCronTransfer()
    # prepare a cursor object using cursor() method
    cursor = db.cursor()

    # Prepare SQL query to INSERT a record into the database.
    sql = "select  sh.id, origen, final, crontab, log, sh.id_conexion,status from share sh inner join conexionssh cs on sh.id_conexion=cs.id;"
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
            "crontab" : row[3],
            "LOG" : row[4],
            "id_conexion": row[5],
            "status": row[6]
            }
            matriz.append(data) 
        return(matriz)
    else:
        return(0)

