import os
from tabulate import tabulate
import connect_db as cdb

def c_ssh():
    db = cdb.DataBase()
    conexiones=db.select_todas_conexiones()
    # Convertir el diccionario en lista
    if conexiones != 0:
        for indice in range(len(conexiones)):
            conexiones[indice]=list(conexiones[indice].values())
        print("")
        print("Conexiones guardanas en el sistema:")
        print("")
        print(tabulate(conexiones, headers=["ID","IP","Puerto","Usuario", "Tipo de autenticación","Ruta clave","Primera conexión"]))
    else:
        print("No hay conexiones en el sistema")
        return(1)


def c_servicio():
    db = cdb.DataBase()
    datos=db.select_todo()
    # Convertir el diccionario en lista
    if datos != 0:
        for indice in range(len(datos)):
            datos[indice]=list(datos[indice].values())
        print("")
        print("Servicios guardados en el sistema:")
        print("")
        print(tabulate(datos, headers=["ID","crontab","tipo transferencia","ruta local","ruta remoto","log","id conexion","status"]))
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