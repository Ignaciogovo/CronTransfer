import funcionesSSH as fssh
import sys
import connect_db as cdb
from datetime import datetime
if len(sys.argv)>=3:
    print("demasiados argumentos")
    sys.exit()
def conexionData():
    # Obtenemos el id  a partir de un parametro
    db=cdb.DataBase()
    try:
        id = sys.argv[2]
    except:
        print("El programa compartir.py no recibe argumentos, fallo en el archivo crontab")
        sys.exit(1)
    try:
        # Vemos si se fuerza a ejecutar el envio
        log=sys.argv[1]
        if log=="a":
            log=db.select_log(id)
    except:
        log=db.select_log(id)
    archivo=fssh.EscritorLog(log)
    # Comprobamos el status del servicio
    try:
        status = db.select_status(id)
    except:
        print("No es posible conexion con la base de datos o los datos no se han encontrado")
        sys.exit(1)
        # Forzar status:
    # if forzado== "f":
    #     status = 'activate'
    # Comprobamos el status del servicio
    if status != 'activate':
        # Cerramos el programa
        print("Esta desactivado \n")
        sys.exit(1)
    try:
        
        origenfinal = db.select_share_origen_final(id)
        idssh= db.select_share_id_conexion(id)
    except:
        mensaje=("No es posible conexion con la base de datos o los datos no se han encontrado")
        print(mensaje)
        archivo.escribir_log(mensaje)
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
    data["log"]=log
    return(data)

def inicio_programa():
    try:
        id = sys.argv[2]
        try:
            # Vemos si se fuerza a ejecutar el envio
            log=sys.argv[1]
        except:
            db=cdb.DataBase()
            log=db.select_log(id)
    except:
        print("No se recibe argumentos, fallo en la ejecución de cron_run o en el en el archivo crontab --->"+str(datetime.now()))
        sys.exit(1)
    # Escribimos en el archivo
    archivo=fssh.EscritorLog(log)
    print("")
    archivo.escribir_log("")
    print("-------------")
    archivo.escribir_log("-------------")
    print(str(datetime.now()))
    archivo.escribir_log(str(datetime.now()))
    print("Inicio transferencia  del servicio:"+str(id))
    archivo.escribir_log("Inicio transferencia  del servicio:"+str(id))
    print("-------------")
    archivo.escribir_log("-------------")

def final_programa(n,n2,data):
    archivo=fssh.EscritorLog(data["log"])
    print("-------------")
    archivo.escribir_log("-------------")
    if n == 1:
        mensaje="Transferecia fallida"
        print(mensaje)
        archivo.escribir_log(mensaje)
    elif n2==2:
        mensaje="Transferencia exitosa, pero no se ha podido borrar archivos comprimidos temporales en la ruta: "+data["SOURCE"]
        print(mensaje)
        archivo.escribir_log(mensaje)
    else:
        mensaje="Transferecia exitosa"
        print(mensaje)
        archivo.escribir_log(mensaje)
    print(str(datetime.now()))
    archivo.escribir_log(str(datetime.now()))
    print("-------------")
    archivo.escribir_log("-------------")
    archivo.escribir_log("")
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
final_programa(control,segundo_control,envio.data)

