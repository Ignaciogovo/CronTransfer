from ast import Return
from genericpath import isdir, isfile
import sys
from datetime import datetime
import os
import funcionesSSH as fs
import cifradopass as cp

data = {}
data["HOST"]=  '192.168.1.131'
data["PORT"] = '22'
data["USER"] = 'abc'
data["TIPO"] = 'password'
data["CLAVE"] = '/home/ignaciogovo/.ssh/prueba/id_prueba'
data["PASS"] = 'abc'
data["SOURCE"]=  '/contenedores/keeweb'#/home/ignaciogovo/proyectos/EstudiosPython/AnalisisDatos'
data["FINAL"] = '/home/abc/prueba.py'

# Control+k control+u  --> Descomenta
#Control+k control+c --> Comenta
# sendfile(data)
# data["PASS"]=cp.encriptar_pass(data["PASS"])
# # data["PASS"]=cp.desencriptar_pass(data["PASS"])
# # print(data["PASS"])
# # fs.comprobarSSH(data)
# fs.realizar_envio(data)


def generarArchivoFecha(data):
    final=(data["FINAL"])[((data["FINAL"]).rfind("/"))+1:]
    #fecha actual
    now = datetime.now()
    now= ("f_"+str(now.year)+str(now.month)+str(now.day)+"_")
    #Datetime
    now=now+final
    data["FINAL"]=data["FINAL"].replace(final,now)
    return(data)
    







# def A_Rutafinal(data):
#     origen=(data["SOURCE"])[((data["SOURCE"]).rfind("/")):]
#     final=(data["FINAL"])[((data["FINAL"]).rfind("/")):]
#     print("")
#     print(origen)
#     print("")
#     print(final)

# A_Rutafinal(data)
# data=fs.A_Compresion(data)
# data=fs.A_Rutafinal(data)
# print(data)
# fs.sendfile(data)



  

# # pruebas(data)
# pruebaruta(data)
