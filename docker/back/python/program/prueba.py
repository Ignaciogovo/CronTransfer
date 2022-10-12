from ast import Return
from genericpath import isdir, isfile
import sys
from datetime import datetime
import os
import funcionesSSH as fs


data = {}
data["HOST"]=  '192.168.1.131'
data["PORT"] = '22'
data["USER"] = 'abc'
data["PASS"] = 'abc'
data["SOURCE"]=  '/home/ignaciogovo/proyectos/EstudiosPython/AnalisisDatos'
data["FINAL"] = '/home/abc/backups'

# Control+k control+u  --> Descomenta
#Control+k control+c --> Comenta
# sendfile(data)


def pruebas(data):
    
    if os.path.isfile(data["SOURCE"]):
        print("Es un archivo -->"+str(data["SOURCE"]))
    else:
        if os.path.isdir(data["SOURCE"]):
            print("Es un fichero->"+str(data["SOURCE"]))
            # Recorremos el fichero
            # try:
            for nombre_directorio, dirs, ficheros in os.walk(data["SOURCE"]):
                if nombre_directorio != data["SOURCE"]:
                    data2=data.copy()
                    data2["SOURCE"]=nombre_directorio
                    data2["FINAL"]=data["FINAL"]+nombre_directorio
                    pruebas(data2)
                for nombre_fichero in ficheros:
                    data3=data.copy()
                    data3["SOURCE"]=data["SOURCE"]+"/"+nombre_fichero
                    data3["FINAL"]=data["FINAL"]+"/"+nombre_fichero
                    print("Es un archivo -->"+data3["SOURCE"])
                    print("Ruta final:"+data3["FINAL"])

        else:
            print("No podemos reconocer el tipo de ruta de origen.")
            # sys.exit(1)


def pruebaruta(data):
    for root, dirs, files in os.walk(data["SOURCE"]):
        for name in files:
            print(os.path.join(root, name))


# def A_Rutafinal(data):
#     origen=(data["SOURCE"])[((data["SOURCE"]).rfind("/")):]
#     final=(data["FINAL"])[((data["FINAL"]).rfind("/")):]
#     print("")
#     print(origen)
#     print("")
#     print(final)

# A_Rutafinal(data)
data=fs.A_Compresion(data)
data=fs.A_Rutafinal(data)
print(data)
fs.sendfile(data)



  

# # pruebas(data)
# pruebaruta(data)
