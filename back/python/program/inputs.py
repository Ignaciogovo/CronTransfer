import ingresos
import crontabs
import connect_db as cdb
import sys
import f_consultas as f_c
from ascii import logo
import re
especiales = ("@reboot","@yearly","@annually","@monthly","@weekly","@daily","@midnight","@hourly")
dias_semana= ("sun","mon","tue","wed","thu","fri","sat")
meses = ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
def comprobacion_crontab(crontab):
    crontab = " ".join(crontab.split())# Eliminamos los posibles dobles espacios
    if crontab in especiales:
        1==1
    else:
        list_comp= re.split(" ", crontab) # Separamos el crontab en una lista a partir de los espacios
        if len(list_comp) == 5:
            1==1
        else:
            print("Formato de crontab erroneo")
            sys.exit()


def crear_conexion():
    db=cdb.DataBase()
    print("")
    print("Introducir una conexión nueva")
    print("")
    # Coger datos de ssh
    datosssh=ingresos.introducirssh()
    # Insertar datos en la base de datos
    db.insert_ssh(datosssh)
    # Coger datos para tabla share
    # Cogemos el id del usuario que hemos escrito anteriormente
    idssh=db.ultimoidssh()
    return(idssh)


def inputcompleto():
    db=cdb.DataBase()
    conexiones=db.select_todas_conexiones()
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
    print("Introducir datos del servicio de de transferencia")
    print("")
    datosshare=ingresos.introducirshare()
    # Añadimos el id del usuario de ssh a los datos de conexión
    datosshare["id_conexion"]=idssh
    # Insertamos datos de share en su tabla
    log=datosshare["log"]
    db.insert_share(datosshare,borrar)
    # Realizar Crontab:
    idshare =db.ultimoidSHARE()
    crontabs.RealizarCrontab(idshare)
    if log != "NULL":
        print("Se guardado la configuración.")
        f = open(log, "x")
        f.close()
        print("La ruta del log de transacciones: "+log)

try:
    menu= sys.argv[1]
    db=cdb.DataBase()
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
        db.insert_ssh(datos_conexion)

    elif menu =="sf":
        try:
            id_conexion= str(sys.argv[2])
            crontab= (str(sys.argv[3])).strip()
            transferencia=str(sys.argv[4])
            transferencia=transferencia.lower()
            localhost= str(sys.argv[5])
            remoto= str(sys.argv[6])
            log = str(sys.argv[7]) or ("NULL")
            sobrescribir = str(sys.argv[8]) or ("N")

        except:
            print("Es necesario incluir todos los parametros")
            print("parametros: cron_crontab id_conexion crontab importar/exportar(i/e) /ruta/local /ruta/remoto log(Y/N) sobrescribir(Y/N) ")
            sys.exit(1)
        comprobacion_crontab(crontab)

        # Modificaciones de los datos antes de la inserción
        if log == "y" or log == "Y":
            idshare =int(db.ultimoidSHARE())+1
            borred_share=int(db.select_deleted_id_share())+1
            if idshare < borred_share:
                idshare=borred_share
            log="/log/servicio_"+str(idshare)+".log"
        else:
            log="NULL"
        if sobrescribir == "N" or sobrescribir =="n":
            sobrescribir="N"
        else:
            sobrescribir="Y"
        if transferencia != "e" and transferencia != "i":
            print("Tipo de transferencia errónea, deben ser i (importar) o e (exportar)")
            sys.exit(1)
        else:
            if transferencia== "e":
                transferencia="export"
            else:
                transferencia="import"

        data= {
        "TRANSFERENCIA": transferencia,
        "local": localhost,
        "remoto": remoto,
        "crontab" : crontab,
        "id_conexion" : id_conexion,
        "log": log,
        "SOBRESCRIBIR": sobrescribir
        }
        ## Modificamos los datos de ruta para evitar errores
        if data["local"].endswith("/"):
            data["local"]=data["local"][:-1]
        # Incluimos el directorio del contenedor para evitar errores
        if data["local"].startswith("/"):
            data["local"]='/source'+data["local"]
        else:
            data["local"]='/source'+"/"+data["local"]

        # configuramos los datos proporcionados
        # Eliminamos el / final para evitar errores
        if data["remoto"].endswith("/"):
            data["remoto"]=data["remoto"][:-1]


        # Insertamos datos de share en su tabla
        db.insert_share(data,None)
        # Realizar Crontab:
        idshare =db.ultimoidSHARE()
        crontabs.RealizarCrontab(idshare)
        if log != "NULL":
            print("Se guardado la configuración.")
            f = open(log, "x")
            f.close()
            print("La ruta del log de transacciones: "+log)
    
    else:
        print("No se reconoce los parametros")