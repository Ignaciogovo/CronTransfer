from pydoc import importfile
import ingresos
import conexionbbdd
import crontabs
import sys
import f_consultas as f_c
from ascii import logo
import re
import prueba_poo
especiales = ("@reboot","@yearly","@annually","@monthly","@weekly","@daily","@midnight","@hourly")
dias_semana= ("sun","mon","tue","wed","thu","fri","sat")
meses = ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
def comprobación_crontab(crontab):
    crontab = " ".join(crontab.split())# Eliminamos los posibles dobles espacios
    if crontab in especiales:
        1==1
    else:
        list_comp= re.split(" ", crontab) # Separamos el crontab en una lista a partir de los espacios
        if len(list_comp) == 5:
            1==1
        else:
            print("Formato de crontab erroneo")
            sys.exit(1)


def crear_conexion():
    print("")
    print("Introducir una conexión nueva")
    print("")
    # Coger datos de ssh
    datosssh=ingresos.introducirssh()
    # Insertar datos en la base de datos
    # db=prueba_poo.DataBase()
    conexionbbdd.insert_ssh(datosssh)
    # db.insert_ssh(datosssh)
    # Coger datos para tabla share
    # Cogemos el id del usuario que hemos escrito anteriormente
    idssh=conexionbbdd.ultimoidssh()
    return(idssh)


def inputcompleto():
    conexiones=conexionbbdd.comprobar_Conexiones()
    # Variable necesaria para la inserción del servicio
    borrar = 1
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
        else:
            borrar = None
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
    log=datosshare["log"]
    conexionbbdd.insert_share(datosshare,borrar)
    # conexionbbdd.insert_share(datosshare,None)
    # Realizar Crontab:
    idshare =conexionbbdd.ultimoidSHARE()
    crontabs.RealizarCrontab(idshare)
    if log != "NULL":
        print("Se guardado la configuración.")
        f = open(log, "x")
        f.close()
        print("La ruta del log de transacciones: "+log)

try:
    menu= sys.argv[1]
except:
    menu = "s"
if menu == "c":
    logo()
    crear_conexion()

elif menu =="s":
    logo()
    inputcompleto()
else:
    if menu =="cf":
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
        conexionbbdd.insert_ssh(datos_conexion)

    elif menu =="sf":
        try:
            id_conexion= str(sys.argv[2])
            crontab= (str(sys.argv[3])).strip()
            comprobación_crontab(crontab)
            origen= str(sys.argv[4])
            final= str(sys.argv[5])
            log = str(sys.argv[6]) or ("NULL")
            if log == "y" or log == "Y":
                idshare =int(conexionbbdd.ultimoidSHARE())+1
                log="/log/servicio_"+str(idshare)+".log"
            else:
                log="NULL"
            sobrescribir = str(sys.argv[7]) or ("N")
            if sobrescribir == "N" or sobrescribir =="n":
                sobrescribir="N"
            else:
                sobrescribir="Y"
        except:
            print("Es necesario incluir todos los parametros")
            print("parametros: cron_crontab id_conexion crontab /ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N) ")
            sys.exit(1)
        data= {
        "SOURCE": origen,
        "FINAL": final,
        "crontab" : crontab,
        "id_conexion" : id_conexion,
        "log": log,
        "SOBRESCRIBIR": sobrescribir
        }
        ## Modificamos los datos de ruta para evitar errores
        if data["SOURCE"].endswith("/"):
            data["SOURCE"]=data["SOURCE"][:-1]
        # Incluimos el directorio del contenedor para evitar errores
        if data["SOURCE"].startswith("/"):
            data["SOURCE"]='/source'+data["SOURCE"]
        else:
            data["SOURCE"]='/source'+"/"+data["SOURCE"]

        # configuramos los datos proporcionados
        # Eliminamos el / final para evitar errores
        if data["FINAL"].endswith("/"):
            data["FINAL"]=data["FINAL"][:-1]


        # Insertamos datos de share en su tabla
        conexionbbdd.insert_share(data,None)
        # conexionbbdd.insert_share(datosshare,None)
        # Realizar Crontab:
        idshare =conexionbbdd.ultimoidSHARE()
        crontabs.RealizarCrontab(idshare)
        if log != "NULL":
            print("Se guardado la configuración.")
            f = open(log, "x")
            f.close()
            print("La ruta del log de transacciones: "+log)
    else:
        print("No se reconoce los parametros")