from dataclasses import replace
from genericpath import isdir, isfile
import paramiko
import sys
from datetime import datetime
import os
import shutil
import cifradopass as cp

# Realiza una conexión al servidor
def comprobarSSH(data):
    if data["TIPO"] =='clave':
        try:
            private_key = paramiko.RSAKey.from_private_key_file(data["CLAVE"])
        except:
            print("Error al localizar la clave privada")
            sys.exit(1)
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        if data["TIPO"] =='clave':
            # Nos conectamos al servidor a partir de las credenciales
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], pkey=private_key)
        # Nos conectamos al servidor a partir de las credenciales
        elif data["TIPO"] =='password':
            password = cp.desencriptar_pass(data["PASS"])
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=password)
        else:
            print("problema")
    except:
        print("error al realizar conexión, la conexión no es válida")
        sys.exit(1)
# Comprobamos que la ruta final es correcta y se puede realizar una conexión
def  comprobarRutaSSH(data):
    if data["TIPO"] =='clave':
        private_key = paramiko.RSAKey.from_private_key_file(data["CLAVE"])
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        if data["TIPO"] =='clave':
            # Nos conectamos al servidor a partir de las credenciales
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], pkey=private_key)
        # Nos conectamos al servidor a partir de las credenciales
        elif data["TIPO"] =='password':
            password= cp.desencriptar_pass(data["PASS"])
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=password)
    except:
        print("error al realizar conexión para comprobar ruta final")
        if data["ZIP"]=="YES":
            borrarZIP(data)
        sys.exit(1)
    # Enviamos el archivo a partir de esta serie de lineas
    try:
        # Realizamos el comando y el resultado lo convertimos en variables
        entrada, salida, error = ssh_client.exec_command('ls '+data["FINAL"])
        # print(salida.read().decode()) # decode hace más legible el texto.
        c_error=error.read().decode()
        ssh_client.close()  
        if (len(c_error)==0):
            return(0)
        else:
            return(1)
    except: 
        print("Error al comprobar la ruta final, destino es incorrecto")
        if data["ZIP"]=="YES":
            borrarZIP(data)
        sys.exit(1)
        # Cerramos conexión



def putdfile(data):
    if data["TIPO"] =='clave':
        private_key = paramiko.RSAKey.from_private_key_file(data["CLAVE"])
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        if data["TIPO"] =='clave':
            # Nos conectamos al servidor a partir de las credenciales
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], pkey=private_key)
        # Nos conectamos al servidor a partir de las credenciales
        elif data["TIPO"] =='password':
            password= cp.desencriptar_pass(data["PASS"])
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=password)
    except:
        print("error al realizar conexión al transferir archivo")
        if data["ZIP"]=="YES":
            borrarZIP(data)
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
        if data["ZIP"]=="YES":
            borrarZIP(data)
        sys.exit(1)
        # Cerramos conexión
    ssh_client.close()

def getfile(data):
    if data["TIPO"] =='clave':
        private_key = paramiko.RSAKey.from_private_key_file(data["CLAVE"])
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) # Con esto indicamos que accedemos con nuestras propias credenciales
    try:
        if data["TIPO"] =='clave':
            # Nos conectamos al servidor a partir de las credenciales
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], pkey=private_key)
        # Nos conectamos al servidor a partir de las credenciales
        elif data["TIPO"] =='password':
            password= cp.desencriptar_pass(data["PASS"])
            ssh_client.connect(hostname=data["HOST"], port=data["PORT"], username=data["USER"], password=password)
    except:
        print("error al realizar conexión al transferir archivo")
        if data["ZIP"]=="YES":
            borrarZIP(data)
        sys.exit(1)
    # Enviamos el archivo a partir de esta serie de lineas
    try:
        sftp_client = ssh_client.open_sftp()
        sftp_client.get(
            data["SOURCE"],
            data["FINAL"]
        )   
        sftp_client.close()
    except: 
        print("Error al transferir archivos, comprueba si la ruta de origen o destino es correcta")
        if data["ZIP"]=="YES":
            borrarZIP(data)
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
            archivo_zip = shutil.make_archive(data["SOURCE"], "zip", data["SOURCE"])
            if os.path.isfile(archivo_zip):
                data["SOURCE"]=archivo_zip
                data["ZIP"] = "YES"
                return(data)
            else:
                print("No se ha podido realizar la compresión")
                sys.exit(1)
        else:
            print("No se ha reconocido si la ruta es un archivo o directorio para decidir si comprimir o no, ¿Es la ruta correcta?")
            sys.exit(1)   

def borrarZIP(data):
    try:
    # Borrar archivo zip
        os.remove(data["SOURCE"])
    except:
        print("No se ha podido borrar el archivo zip creado temporalmente")

def A_Rutafinal(data):
    origen=(data["SOURCE"])[((data["SOURCE"]).rfind("/")):]
    final=(data["FINAL"])[((data["FINAL"]).rfind("/")):]
    valorfinal=comprobarRutaSSH(data)
    # Si la ruta es correcta le añadimos a la ruta el archivo origen
    if valorfinal==0:
        data["FINAL"]=data["FINAL"]+origen
        # Si la ruta es incorrecta cambiamos el dato final por el dato origen
    else:
        data["FINAL"]=data["FINAL"].replace(final,origen)
    return(data)

def realizar_envio(data):
    #Analizamos los datos que se envian, para proporcionar la forma adecuada de envio
    data=A_Compresion(data)
    #Analizamos la ruta final para proporcionar la forma adecuada de envio
    data=A_Rutafinal(data)
    if data["SOBRESCRIBIR"]=="N":
        data=generarArchivoFecha(data)
    # Realizamos envio
    if 1==1:
        putdfile(data)
    else:
        getfile()
    #Borramos el archivo zip
    borrarZIP(data)


def generarArchivoFecha(data):
    final=(data["FINAL"])[((data["FINAL"]).rfind("/"))+1:]
    #fecha actual
    now = datetime.now()
    now= ("f_"+str(now.year)+str(now.month)+str(now.day)+"_"+str(now.hour)+str(now.minute)+"_")
    #Datetime
    now=now+final
    data["FINAL"]=data["FINAL"].replace(final,now)
    return(data)



