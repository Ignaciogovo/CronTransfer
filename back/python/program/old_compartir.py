import sys
import connect_db as cdb
import oldfuncionesSSH as fssh
from datetime import datetime
def conexionData():
    print("-------------")
    print("Inicio backup  --->"+str(datetime.now()))
    print("-------------")
    # Obtenemos el id  a partir de un parametro
    db=cdb.DataBase()
    try:
        id = sys.argv[1]
    except:
        print("El programa compartir.py no recibe argumentos, fallo en el archivo crontab")
        sys.exit(1)
    try:
        # Vemos si se fuerza a ejecutar el envio
        forzado=sys.argv[2]
    except:
        forzado="0"
    # Comprobamos el status del servicio
    try:
        status = db.select_status(id)
    except:
        print("No es posible conexion con la base de datos o los datos no se han encontrado")
        sys.exit(1)
        # Forzar status:
    if forzado== "f":
        status = 'activate'
    # Comprobamos el status del servicio
    if status != 'activate':
        # Cerramos el programa
        print("Esta desactivado \n")
        sys.exit(1)
    try:
        
        origenfinal = db.select_share_origen_final(id)
        idssh= db.select_id_conexion_fromshare(id)
    except:
        print("No es posible conexion con la base de datos o los datos no se han encontrado")
        sys.exit(1)
    try:
        data= db.select_datos_ssh(idssh)
    except:
        print("Problemas al sacar datos a partir del idSSH")    
        sys.exit(1)
    data["SOURCE"] =origenfinal[0]
    data["FINAL"] =origenfinal[1]
    data["SOBRESCRIBIR"] =origenfinal[2]
    return(data)

data=conexionData()
try:
    fssh.realizar_envio(data)
    print("Finalizado backup  --->"+str(datetime.now()))
    print("")
except:
    print("No se ha podido enviar el archivo")
    print("")
    sys.exit(1)