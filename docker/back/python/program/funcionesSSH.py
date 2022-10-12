from genericpath import isdir, isfile
import paramiko
import sys
from datetime import datetime
import os
import shutil
def comprobarSSH(data):
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        # Nos conectamos al servidor a partir de las credenciales
        ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=data["PASS"])
    except:
        print("error al realizar conexión, la conexión no es válida")
        sys.exit(1)

def  comprobarRutaSSH(data):
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
        # Realizamos el comando y el resultado lo convertimos en variables
        entrada, salida, error = ssh_client.exec_command('ls '+data["FINAL"])
        # print(salida.read().decode()) # decode hace más legible el texto.
        c_error=error.read().decode()
        if (len(c_error)==0):
            return(0)
        else:
            return(1)
    except: 
        print("Error al comprobar la ruta, destino es correcta")
        sys.exit(1)
        # Cerramos conexión
    ssh_client.close()



def sendfile(data):

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
        print("Error al transferir archivos, comprueba si la ruta de origen o destino es correcta")
        sys.exit(1)
        # Cerramos conexión
    ssh_client.close()


# Analizamos si es necesario la compresión para realizar el envio
def A_Compresion(data):
    if os.path.isfile(data["SOURCE"]):
        print("Es un fichero por lo que no realizamos compresión")
        return(data)
    else:
        if os.path.isdir(data["SOURCE"]):
            archivo_zip = shutil.make_archive("/home/ignaciogovo/AnalisisDatos", "zip", data["SOURCE"])
            if os.path.isfile(archivo_zip):
                data["SOURCE"]=archivo_zip
                return(data)
            else:
                print("No se ha podido realizar la compresión")
                sys.exit(1)
        else:
            print("No se ha reconocido si la ruta es un archivo o directorio para decidir si comprimir o no")
            sys.exit(1)   


def A_Rutafinal(data):
    origen=(data["SOURCE"])[((data["SOURCE"]).rfind("/")):]
    final=(data["FINAL"])[((data["SOURCE"]).rfind("/")):]
    valorfinal=comprobarRutaSSH(data)
    # Si la ruta es correcta le añadimos a la ruta el archivo origen
    if valorfinal==0:
        data["FINAL"]=data["FINAL"]+origen
        # Si la ruta es incorrecta cambiamos el dato final por el dato origen
    else:
        data["FINAL"]=data["FINAL"].replace(final,origen)
    return(data)

# def generarArchivoFecha(archivo):
#     #fecha actual
#     now = datetime.now()
#     #Datetime
#     if
#         now.day
#         now.month
#         now.year
