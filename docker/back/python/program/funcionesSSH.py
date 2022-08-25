from genericpath import isdir, isfile
import paramiko
import sys
from datetime import datetime
import os
def comprobarSSH(data):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        # Nos conectamos al servidor a partir de las credenciales
        ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=data["PASS"])
    except:
        print("error al realizar conexión, la conexión no es válida")
        sys.exit(1)


def sendfile(data):
        # Introducimos los datos

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        # Nos conectamos al servidor a partir de las credenciales
        ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=data["PASS"])
    except:
        print("error al realizar conexión")
        sys.exit(1)
    # Enviamos el archivo a partir de esta serie de lineas
    try:
        sftp_client = ssh_client.open_sftp()
        sftp_client.put(
            data["SOURCE"],
            data["FINAL"]
        )   
        sftp_client.close()
    except: 
        print("Error al transferir archivos")
        sys.exit(1)
        # Cerramos conexión
    ssh_client.close()

# Con esta función analizamos la ruta para conocer si es un archivo o un directorio. Según lo que sea se ejeturá distintas
def analizarRuta(data):
    if os.path.isfile(data["SOURCE"]):
        sendfile(data["SOURCE"])
    else:
        if os.path.isdir(data["SOURCE"]):
            with os.scandir(data["SOURCE"]) as ficheros:
                for fichero in ficheros:
                    if data["SOURCE"].endswith('/'): 
                        data["SOURCE"] = data["SOURCE"]+fichero
                    else:    
                        data["SOURCE"] = data["SOURCE"]+'/'+fichero
                    analizarRuta(data)
        else:
            print("No podemos reconocer el tipo de ruta de origen.")
            sys.exit(1)

# def generarArchivoFecha(archivo):
#     #fecha actual
#     now = datetime.now()
#     #Datetime
#     if
#         now.day
#         now.month
#         now.year
