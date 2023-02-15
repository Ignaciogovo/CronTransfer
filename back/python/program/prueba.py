import prueba_poo as pp
import sys
import os
from tabulate import tabulate

def c_ssh():
    bd = pp.DataBase()
    conexiones=bd.select_todas_conexiones()
    # Convertir el diccionario en lista
    if conexiones != 0:
        for indice in range(len(conexiones)):
            conexiones[indice]=list(conexiones[indice].values())
        print("")
        print("Conexiones guardanas en el sistema:")
        print("")
        print(tabulate(conexiones, headers=["ID","IP","PORT","USER", "Tipo","first connection"]))
    else:
        print("No hay conexiones en el sistema")
        return(1)


def c_servicio():
    bd = pp.DataBase()
    datos=bd.select_servicios()
    # Convertir el diccionario en lista
    if datos != 0:
        for indice in range(len(datos)):
            datos[indice]=list(datos[indice].values())
        print("")
        print("Servicios guardados en el sistema:")
        print("")
        print(tabulate(datos, headers=["ID","origen","final","crontab","log","id_conexion","status"]))
    else:
        print("No hay servicios almacenados en el sistema")
        return(1)



def contar_logs():
    total = 0
    directorio= "/log"
    for path in os.listdir(directorio):
        if str(path).find("."):
            total= total+1
    return(total)


try:
    menu= sys.argv[1]
except:
    menu = "a"
if menu == "c":
    c_ssh()

elif menu =="s":
    c_servicio()

elif menu == "a":
    c_ssh()
    print("")
    print("---------------")
    print("")
    c_servicio()

else:
    print("No se reconoce los parametros")
 
