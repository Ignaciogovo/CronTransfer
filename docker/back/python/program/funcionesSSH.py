import paramiko
import sys

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
