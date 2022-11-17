import conexionbbdd as cb
import os
from tabulate import tabulate

def c_ssh():
    conexiones=cb.comprobar_Conexiones()
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
    datos=cb.consultar_Servicio()
    # Convertir el diccionario en lista
    if datos != 0:
        for indice in range(len(datos)):
            datos[indice]=list(datos[indice].values())
        print("")
        print("Servicios guardados en el sistema:")
        print("")
        print(tabulate(datos, headers=["ID","origen","final","log","id_conexion","IP", "user"]))
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