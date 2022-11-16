from pydoc import importfile
import ingresos
import conexionbbdd
import crontabs
import sys
import f_consultas as f_c
from ascii import logo


def crear_conexion():
    print("")
    print("Introducir una conexión nueva")
    print("")
    # Coger datos de ssh
    datosssh=ingresos.introducirssh()
    # Insertar datos en la base de datos
    conexionbbdd.ingresarSSH(datosssh)
    # Coger datos para tabla share
    # Cogemos el id del usuario que hemos escrito anteriormente
    idssh=conexionbbdd.ultimoidssh()
    return(idssh)


def inputcompleto():
    conexiones=conexionbbdd.comprobar_Conexiones()
    if conexiones != 0:
        print("Hay conexiones guardadas en el sistema")
        print("1- Usar una conexión ya guardada en el sistema")
        print("2- Crear una conexión")
        opcion_menu = input("Escoger 1 o 2 :(Por defecto se crea un usuario nuevo): ") or ("2")

    else:
        opcion_menu = "2"

    if opcion_menu == "1":
        f_c.c_ssh()
        idssh = input("Introducir ID de la conexión deseada: (Si introduce el 0 crea una nueva conexión: ") or ("0")
        if idssh == "0":
            idssh=crear_conexion()
    # Creamos una nueva conexion
    elif opcion_menu == "2":
            idssh=crear_conexion()


    print("")
    print("Introducir datos del servicio de backup")
    print("")
    datosshare=ingresos.introducirshare()
    # Añadimos el id del usuario de ssh a los datos de conexión
    datosshare["id_conexion"]=idssh
    # Insertamos datos de share en su tabla
    conexionbbdd.ingresarShare(datosshare,1)
    # conexionbbdd.ingresarShare(datosshare,None)
    # Realizar Crontab:
    idshare =conexionbbdd.ultimoidSHARE()
    crontabs.RealizarCrontab(idshare)

try:
    menu= sys.argv[1]
except:
    print("Es necesario incluir un argumento")
    sys.exit(1)
if menu == "c":
    logo()
    crear_conexion()

elif menu =="s":
    logo()
    inputcompleto()
elif menu =="cf":
    try:
        data={}
        data["HOST"]=sys.argv[2]
        data["PORT"] = sys.argv[3]
        data["USER"] = sys.argv[4]
        data["TIPO"] = sys.argv[5]
    except:
        print("Es necesario incluir más parametros")
        sys.exit(1)
    datos_conexion=ingresos.fast_introducirssh(data)
    conexionbbdd.ingresarSSH(datos_conexion)
    
else:
    print("No se reconoce los parametros")