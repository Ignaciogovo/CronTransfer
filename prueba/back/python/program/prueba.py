# # from ast import Return
# # from genericpath import isdir, isfile
# # import sys
# # from datetime import datetime
# # import os
# # import funcionesSSH as fs
# # import cifradopass as cp
# from tabulate import tabulate
# import sys
import re
# # data = {}
# # data["HOST"]=  
# # data["PORT"] = '22'
# # data["USER"] = 'abc'
# # data["TIPO"] = 
# # data["CLAVE"] = 
# # data["PASS"] = 
# # data["SOURCE"]=  '/prueba'
# # data["FINAL"] = '/home/abc'

# # Control+k control+u  --> Descomenta
# #Control+k control+c --> Comenta
# # sendfile(data)
# # data["PASS"]=cp.encriptar_pass(data["PASS"])
# # # data["PASS"]=cp.desencriptar_pass(data["PASS"])
# # # print(data["PASS"])
# # # fs.comprobarSSH(data)
# # fs.realizar_envio(data)


# # def generarArchivoFecha(data):
# #     final=(data["FINAL"])[((data["FINAL"]).rfind("/"))+1:]
# #     #fecha actual
# #     now = datetime.now()
# #     now= ("f_"+str(now.year)+str(now.month)+str(now.day)+"_")
# #     #Datetime
# #     now=now+final
# #     data["FINAL"]=data["FINAL"].replace(final,now)
# #     return(data)
    


# hora= str(sys.argv[1])
# if int(hora) not in range(0,24):
#     print("La hora no es válida")
#     sys.exit(1)



# d = [ ["Mark", 12, 95],
#      ["Jay", 11, 88],
#      ["Jack", 14, 90]]

# print(tabulate(d, headers=["Name", "Age", "Percent"]))


# # now = datetime.now()
# # now= ("f_"+str(now.year)+str(now.month)+str(now.day)+"_"+str(now.hour)+str(now.minute)+"_")
# # print(now)

# # print("Finalizado backup  --->"+str(datetime.now()))



# # def A_Rutafinal(data):
# #     origen=(data["SOURCE"])[((data["SOURCE"]).rfind("/")):]
# #     final=(data["FINAL"])[((data["FINAL"]).rfind("/")):]
# #     print("")
# #     print(origen)
# #     print("")
# #     print(final)

# # A_Rutafinal(data)
# # data=fs.A_Compresion(data)
# # data=fs.A_Rutafinal(data)
# # print(data)
# # fs.sendfile(data)



  

# # # pruebas(data)
# # pruebaruta(data)




comprobación_crontab("* * * feb,jun,oct *")




#ejemplo crontab

# 0 0 * * *
# 0 6,18 * * *
# 0 */6 * * *
# */10 * * * *
# 0 * 20 7 *
# @reboot 
# * * * feb,jun,oct *
# 0 19 * * mon
#
#
#
#
#
#


# https://crontab.guru comprueba los crontab


 
