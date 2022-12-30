# importar recursos
from cryptography.fernet import Fernet

# Función para escribir y guardar la clave:

def genera_clave():
    clave = Fernet.generate_key()
    with open("/.claves/clave.key","wb") as archivo_clave:
        archivo_clave.write(clave)

# Función para cargar la clave
def cargar_clave():
    return open("/.claves/clave.key","rb").read()


# Encriptar un mensaje
def encriptar_pass(pswd):
    clave = cargar_clave()
    pswd = pswd.encode()
    # Iniciamos "Fernet" 
    f = Fernet(clave)
    # Encriptamos mensaje
    encriptado = f.encrypt(pswd)
    return(encriptado)


def desencriptar_pass(pswd):
    clave = cargar_clave()
    f = Fernet(clave)
    # Desencriptar mensaje
    desencriptado = f.decrypt(pswd)
    desencriptado=desencriptado.decode()
    return(desencriptado)