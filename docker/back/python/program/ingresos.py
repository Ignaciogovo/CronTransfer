from multiprocessing.sharedctypes import Value
import sys
from time import sleep
from getpass import getpass
from pymysql import NULL
from funcionesSSH import comprobarSSH
import cifradopass as cp
def introducirssh():
    data={}
    data["HOST"]=  input("IP Servidor: ") or ("")
    data["PORT"] = input("puerto(puerto 22 por defecto): ") or ("22")
    data["USER"] = input("usuario: ") or ("")
    print("Qué tipo de seguridad en la conexión quieres usar?:")
    print("1- password")
    print("2- clave privada")
    data["TIPO"] = input("Indique el número:(Por defecto 1)") or ("1")
    if data["TIPO"] == 1:
        data["PASS"]= getpass("Contraseña: ")
        data["PASS"]= cp.ecriptar_pass(data["PASS"])
        data["CLAVE"]= 'NULL'
        data["TIPO"] = 'password'
    elif data["TIPO"]==2:
        data["PASS"]= 'NULL'
        data["CLAVE"]= input("Ruta clave privada: ")
        data["TIPO"] = 'clave'
    else:
        print("No has seleccionado ninguna opción de las anteriores")
        sys.exit(1)   
    validar(data)
    comprobar(data)
    comprobarSSH(data)
    return(data)
def introducirshare():
    data={}
    data["SOURCE"]=  input("Ruta origen: ") or ("")
    # configuramos los datos proporcionados
    # Eliminamos el / final para evitar errores
    if data["SOURCE"].endswith("/"):
       data["SOURCE"]=data["SOURCE"][:-1]
    # Incluimos el directorio del contenedor para evitar errores
    if data["SOURCE"].startswith("/"):
        data["SOURCE"]='/source'+data["SOURCE"]
    else:
        data["SOURCE"]='/source'+"/"+data["SOURCE"]
    data["FINAL"] = input("rutafinal: ") or ("")
    # configuramos los datos proporcionados
    # Eliminamos el / final para evitar errores
    if data["FINAL"].endswith("/"):
       data["FINAL"]=data["FINAL"][:-1]
    print("")
    print("Introducir fechas y horarios del backups:")
    data["minutes"] ='Falso'
    while data["minutes"] =='Falso':
        print("")
        print("Elegir minutos:")
        sleep(0.5)
        print("Eliga una letra si desea: \n a: Cada minuto. \n b: Minutos pares. \n c: Minutos impares. \n d: Cada 5 minutos. \n e: Cada 30 minutos. \n De lo contrario si desea hacerlo en un minuto especifico introduzca el número. (0/59)")
        data["minutes"] = input("minutos: ") or ("")
        data["minutes"]=validarIndividual('minutes',data["minutes"])
    data["hours"] = 'Falso'
    while data["hours"] == 'Falso':
        print("")
        print("Elegir Horas:")
        sleep(0.5)
        print("Eliga una letra si desea: \n a: Cada hora. \n b: Cada 2 horas. \n c: cada hora inpar. \n d: Cada 3 horas. \n e: Cada 6 horas. \n f: cada 12 horas. \n De lo contrario si desea hacerlo en una hora especifica introduzca el número. (0/23)")
        data["hours"] = input("horas: ") or ("")
        data["hours"]=validarIndividual('hours',data["hours"])
    data["days"] = 'Falso'    
    while data["days"] == 'Falso':    
        print("")
        print("Elegir días:")
        sleep(0.5)
        print("Eliga una letra si desea: \n a: Cada dia. \n b: Cada 2 dias. \n c: cada dia inpar. \n d: Cada 5 dias. \n e: Cada 15 días. \n f: cada 30 días. \n De lo contrario si desea hacerlo en un dia especifico del mes introduzca el número. (1/31)")
        data["days"] = input("dias: ") or ("")
        data["days"]=validarIndividual('days',data["days"])
    data["months"]='Falso'    
    while data["months"]=='Falso':
        print("")
        print("Elegir Meses:")
        sleep(0.5)
        print("Eliga una letra si desea: \n a: Cada mes. \n b: Cada 2 meses. \n c: cada mes inpar. \n d: Cada 3 meses. \n De lo contrario si desea hacerlo en un mes especifico introduzca el número. (1/12)")   
        data["months"] = input("meses: ") or ("")
        data["months"]=validarIndividual('months',data["months"])
    data["weekday"]='Falso'    
    while data["weekday"]=='Falso':
        print("")
        print("Elegir día de la semana:")
        sleep(0.5)
        print("Eliga una letra si desea: \n a: cada dia. \n b: Días laborables. \n c: Fin de semana. \n d: Sabado y Domingo. \n De lo contrario si desea hacerlo en dia de la semana especifico especifico introduzca el número. (0/6)")   
        data["weekday"] = input("dias de la semana: ") or ("")
        data["weekday"] = validarIndividual('weekday',data["weekday"])
    sleep(0.5)

    # Preguntamos si quiere guardar un log de transacciones
    print("")
    print("Quieres almacenar el log de transacciones en la ruta /log?(Y/N)")
    data["log"]= input()
    if data["log"] == "y" or data["log"] == "Y":
        data["log"]=input("Indica la ruta del log: ")
    else:
        data["log"]='NULL'
    validar(data)
    comprobar(data)
    return(data)
def validarIndividual(key,valor):
    try:
        valor = int(valor)
        if key == "minutes":
            if valor in range(0,60):
                return(valor)
            else:
                print("valor no valido:")
                return('Falso')
        else:
            if key == "hours":
                if valor in range(0,24):
                    return(valor)
                else:
                    print("valor no valido:")
                    return('Falso')
            else: 
                if key == "days":
                    if valor in range(1,32):
                        return(valor)
                    else:
                        print("valor no valido:")
                        return('Falso')
                else:
                    if key == "months":
                        if valor in range(1,13):
                            return(valor)
                        else:
                            print("valor no valido:")
                            return('Falso')
                    else:
                        if key == "weekday":
                            if valor in range(0,7):
                                return(valor)
                            else:
                                print("valor no valido:")
                                return('Falso')
    except:
        if valor in ['a','A','b','B','c','C','d','D','e','E','f','F']:
            if valor == 'a' or valor == 'A':
                return('*')
            else:
                if valor == 'b' or valor == 'B':
                    if key in ["minutes","hours","days","months"]:
                        return('*/2')
                    else:
                        if key == "weekday":
                            return('1-5')
                        else:
                            print("valor no valido:")
                            return('Falso')
                else:
                    if valor == 'c' or valor== 'C':
                            if key == "minutes":
                                return('1-59/2')
                            else:
                                if key == "hours":
                                    return('1-23/2')
                                else: 
                                    if key == "days":
                                        return('1-31/3')
                                    else:
                                        if key == "months":
                                            return('1-11/2')
                                        else:
                                            if key == "weekday":
                                                return('0,5,6')
                                            else:
                                                print("valor no valido:")
                                                return('Falso')
                    else:
                        if valor == 'd' or valor== 'D':
                            if key == "minutes":
                                return('*/5')
                            else:
                                if key == "hours":
                                    return('*/3')
                                else: 
                                    if key == "days":
                                        return('*/5')
                                    else:
                                        if key == "months":
                                            return('*/3')
                                        else:
                                            if key == "weekday":
                                                return('0,6')
                                            else:
                                                print("valor no valido:")
                                                return('Falso')
                        else:
                            if valor == 'e' or valor== 'E':
                                if key == "minutes":
                                    return('*/30')
                                else:
                                    if key == "hours":
                                        return('*/6')
                                    else: 
                                        if key == "days":
                                            return('*/15')
                                        else:
                                            print("valor no valido:")
                                            return('Falso')
                            else:
                                    if key == "hours":
                                        return('*/12')
                                    else: 
                                        if key == "days":
                                            return('1')
                                        else:
                                            print("valor no valido:")
                                            return('Falso')
        else:
            print("valor no valido:")
            return('Falso')
def validar(data):
    if "" in data.values():
        print("No has introducido todos los datos necesarios")
        sys.exit(1)

def comprobar(data):
    print("Esto son los datos que desea introducir:")
    for x in data:
        valor = data.get(x)
        # No sacamos por pantalla el valor contraseña
        if  x != "PASS":
            if x == "SOURCE":
                print(x," --> ",valor.replace("/source",""))
            else:
                print(x," --> ",valor)
    comprobar=input("¿Ésta de acuerdo (Y/N)?:")
    if comprobar == "y" or comprobar == "Y":
        print("Realizamos inserción")
    else:
        print("No realizamos inserción")
        sys.exit(1)

def ConvertSTR(data):
    for x in data:
        data[x]= str(data.get(x))
    return data
