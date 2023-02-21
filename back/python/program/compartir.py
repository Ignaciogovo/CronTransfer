import funcionesSSH as fssh
import sys
import connect_db as cdb
from datetime import datetime

def conexionData():
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
        idssh= db.select_share_id_conexion(id)
    except:
        print("No es posible conexion con la base de datos o los datos no se han encontrado")
        sys.exit(1)
    try:
        data= db.select_datos_ssh(idssh)
    except:
        print("Problemas al sacar datos a partir del idSSH")    
        sys.exit(1)
    data["TRANSFERENCIA"] =origenfinal[0]
    data["SOURCE"] =origenfinal[1]
    data["FINAL"] =origenfinal[2]
    data["SOBRESCRIBIR"] =origenfinal[3]
    return(data)

def inicio_programa():
    try:
        id = sys.argv[1]
    except:
        print("No se recibe argumentos, fallo en la ejecución de cron_run o en el en el archivo crontab --->"+str(datetime.now()))
        sys.exit(1)
    print("")
    print("-------------")
    print("Inicio transferencia  del servicio:"+str(id)+" --->"+str(datetime.now()))
    print("-------------")

def final_programa(n,n2,ruta):
    print("-------------")
    if n == 1:
        print("Transferecia fallida -->"+str(datetime.now()))
    elif n2==2:
        print("Transferencia exitosa, pero no se ha podido borrar archivos comprimidos temporales en la ruta: "+ruta+" --->"+str(datetime.now()))
    else:
        print("Transferencia exitosa -->"+str(datetime.now()))
    print("-------------")
    print("")
    sys.exit(1)









# Iniciamos el programa
inicio_programa()
# Nombramos la variable control para comprobar el estado de fallos del programa
control=0
# Si control es en algún momento 1, se corta el programa
while True:
    data=conexionData()
    envio=fssh.operations_transfer(data)
    control=envio.check_connect()
    if control==1:
        break
    control=envio.check_formato_ruta()
    if control=="directorio":
        control=envio.create_zip()
    if control==1:
        break
    control=envio.configuracion_ruta_final()
    if control==1:
        break
    if data["SOBRESCRIBIR"]=="N":
        control=envio.generarArchivoFecha()
        if control==1:
            break
    control=envio.transfer_file()
    break


# Procesos finales
# Borramos el archivo zip temporal
segundo_control=envio.drop_zip()
# Cerramos la conexión ssh por si acaso
envio.disconnect()
final_programa(control,segundo_control,envio.data["SOURCE"])

