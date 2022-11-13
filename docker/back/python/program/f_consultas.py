import conexionbbdd as cb
import os
from tabulate import tabulate

def c_ssh():
    conexiones=cb.comprobar_Conexiones()
    if conexiones != 0:

        print("Estas son las conexiones guardanas en el sistema:")
        # print("ID -------- IP -------- PORT -------- USER -------- fecha_creación_conexión")
        print(tabulate(conexiones, headers=["ID","IP","PORT","USER", "Tipo","first connection"]))
        # for conexion in conexiones:
        #     print(str(conexion["ID"])+" --- "+str(conexion["IP"])+" --- "+str(conexion["PORT"])+" --- "+str(conexion["USER"])+" --- "+str(conexion["FECHA"]))
    else:
        print("No hay conexiones en el sistema")
        return(1)


def c_servicio():
    datos=cb.consultar_Servicio()
    if datos != 0:
        print("Servicios en uso:")
        print(tabulate(datos, headers=["ID","origen","final","IP", "user"]))
        # print("id ------------ origen ----------- final ----------- IP ----------- user")
        # for data in datos:
        #     print(str(data["ID"])+" --- "+str(data["SOURCE"])+" --- "+str(data["FINAL"])+" --- "+(data["IP"])+" --- "+(data["USER"]))
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