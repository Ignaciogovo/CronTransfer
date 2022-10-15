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
data["PASS"] = 'abc'
data["SOURCE"]=  '/home/ignaciogovo/proyectos/EstudiosPython/AnalisisDatos'
data["FINAL"] = '/home/abc/backups'

# Control+k control+u  --> Descomenta
#Control+k control+c --> Comenta
# sendfile(data)


encriptado=cp.ecriptar_pass("hola me llamo paco")
print(encriptado)
desencriptado=cp.desencriptar_pass(encriptado)
print(desencriptado)





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
