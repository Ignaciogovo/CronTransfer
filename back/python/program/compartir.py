import f_SSH as fssh
import sys
import connect_db as cdb
from datetime import datetime
if len(sys.argv)>3:
    print("demasiados argumentos")
    sys.exit()
if len(sys.argv)<3:
    print("Falta argumentos")
    sys.exit()

def comprobacion_status(id,log):
    db=cdb.DataBase()
    archivo=fssh.EscritorLog(log)
    try:
        status = db.select_status(id)
    except:
        mensaje=("No es posible conexion con la base de datos o los datos no se han encontrado para comprobar su estado")
        print(mensaje)
        archivo.escribir_log(mensaje)
        sys.exit(1)
    if status != 'activate':
    # Cerramos el programa
        mensaje=("Esta desactivado \n")
        print(mensaje)
        archivo.escribir_log(mensaje)
        sys.exit(1)
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
        log=str(sys.argv[1])
        if log=="a":
            log=db.select_log(id)
        elif log == "NULL":
            log=db.select_log(id)
            comprobacion_status(id,log)
        else:
            comprobacion_status(id,log)
    except:
        log=db.select_log(id)
    archivo=fssh.EscritorLog(log)
    # Comprobamos el status del servicio

    try:
        origenfinal = db.select_share_origen_final(id)
        idssh= db.select_id_conexion_fromshare(id)
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
    if data["TRANSFERENCIA"]== "export":
        data["SOURCE"] =origenfinal[1]
        data["FINAL"] =origenfinal[2]
    else:
        data["SOURCE"] =origenfinal[2]
        data["FINAL"] =origenfinal[1]
    data["SOBRESCRIBIR"] =origenfinal[3]
    data["log"]=log
    if data["TIPO"]=="clave":
        if data["PASS"]=="NULL":
            data["PASS"]=None
    mensaje="Servicio id: "+str(id)+"\n"
    mensaje=mensaje+"Conexión servidor remoto id: "+str(idssh)+"\n"
    if data["TRANSFERENCIA"] == "export":
            mensaje=mensaje+"Tipo de transferencia: Exportar\n"
    else:
        mensaje=mensaje+"Tipo de transferencia: Importar\n"
    print(mensaje)
    archivo.escribir_log(mensaje)
    
    return(data)

def inicio_programa():
    db=cdb.DataBase()
    try:
        id = sys.argv[2]
        try:
            log=str(sys.argv[1])
        except:
            log=db.select_log(id)
    except:
        print("No se recibe argumentos, fallo en la ejecución de cron_run o en el en el archivo crontab --->"+str(datetime.now()))
        sys.exit(1)
    # Escribimos en el archivo
    if db.check_id_exists_from_share(id)==1:
        print("Este servicio no está guardado en el sistema: "+str(id))
        sys.exit(1)
    if log=="a":
        log=db.select_log(id)
    elif log == "NULL":
        log=db.select_log(id)
    archivo=fssh.EscritorLog(log)
    mensaje="\n-------------\nFecha/Hora: "+str(datetime.now())+"\nInicio transferencia"
    print(mensaje)
    archivo.escribir_log(mensaje)

def final_programa(n,n2,data):
    archivo=fssh.EscritorLog(data["log"])
    if n == 1:
        mensaje="ERROR, transferencia fallida\n"
    else:
        mensaje="Transferecia exitosa\n"
    if n2==2 and n==0:
        mensaje="Transferencia exitosa, pero no se ha podido borrar archivos comprimidos temporales en la ruta: "+data["SOURCE"]+"\n"
    

    mensaje=mensaje+"Fecha/Hora: "+str(datetime.now())+"\n-------------\n"

    print(mensaje)
    archivo.escribir_log(mensaje)
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

