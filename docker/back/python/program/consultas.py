import conexionbbdd as cb
import sys

def c_ssh():
    conexiones=cb.comprobar_Conexiones()
    if conexiones != 0:
        print("Estas son las conexiones guardanas en el sistema:")
        print("ID -------- IP -------- PORT -------- USER -------- fecha_creación_conexión")
        for conexion in conexiones:
            print(str(conexion["ID"])+" --- "+str(conexion["IP"])+" --- "+str(conexion["PORT"])+" --- "+str(conexion["USER"])+" --- "+str(conexion["FECHA"]))
    else:
        print("No hay conexiones en el sistema")


def c_servicio():
    datos=cb.consultarParaborrados()
    if datos != 0:
        print("Servicios en uso:")
        print("id ------------ origen ----------- final ----------- IP ----------- user")
        for data in datos:
            print(str(data["ID"])+" --- "+str(data["SOURCE"])+" --- "+str(data["FINAL"])+" --- "+(data["IP"])+" --- "+(data["USER"]))
    else:
        print("No hay servicios almacenados en el sistema")


try:
    menu= sys.argv[1]
except:
    print("Es necesario incluir un argumento")
    sys.exit(1)
if menu == "1":
    c_ssh()

elif menu =="2":
    c_servicio()

elif menu == "3":
    c_ssh()
    print("")
    print("---------------")
    print("")
    c_servicio()

else:
    print("No se reconoce los argumentos")






