import sys
from time import sleep

from pymysql import NULL
def introducirssh():
    data={}
    data["HOST"]=  input("IP Servidor: ") or ("")
    data["PORT"] = input("puerto: ") or ("")
    data["USER"] = input("usuario: ") or ("")
    data["PASS"] = input("Contraseña: ") or ("")
    validar(data)
    comprobar(data)
    return(data)
def introducirshare():
    data={}
    data["source"]=  input("Ruta origen: ") or ("")
    data["final"] = input("rutafinal: ") or ("")
    print("Introducir fechas y horarios del backups:")
    print("Elegir minutos:")
    sleep(0.5)
    print("Eliga una letra si desea: \n a: Cada minuto. \n b: Cada 2 minutos. \n c: Cada 5 minutos. \n d: Cada 30 minutos. \n e: cada 60 minutos. \n De lo contrario si desea hacerlo en un minuto especifico introduzca el número. (0/59)")
    data["minutes"] = input("minutos: ") or ("")
    print("Elegir Horas:")
    sleep(0.5)
    print("Eliga una letra si desea: \n a: Cada hora. \n b: Cada 2 horas. \n c: cada hora inpar. \n d: Cada 3 horas. \n e: Cada 6 horas. \n f: cada 12 horas. \n De lo contrario si desea hacerlo en una hora especifica introduzca el número. (0/23)")
    data["hours"] = input("horas: ") or ("")
    print("Elegir días:")
    sleep(0.5)
    print("Eliga una letra si desea: \n a: Cada dia. \n b: Cada 2 dias. \n c: cada dia inpar. \n d: Cada 5 dias. \n e: Cada 15 días. \n f: cada 30 días. \n De lo contrario si desea hacerlo en un dia especifico del mes introduzca el número. (1/31)")
    data["days"] = input("dias: ") or ("")
    print("Elegir Meses:")
    sleep(0.5)
    print("Eliga una letra si desea: \n a: Cada mes. \n b: Cada 2 meses. \n c: cada mes inpar. \n d: Cada 3 meses. \n De lo contrario si desea hacerlo en un mes especifico introduzca el número. (1/12)")   
    data["months"] = input("meses: ") or ("")
    print("Elegir día de la semana:")
    sleep(0.5)
    print("Eliga una letra si desea: \n a: cada dia. \n b: Días laborables. \n c: Fin de semana. \n d: Sabado y Domingo. \n De lo contrario si desea hacerlo en dia de la semana especifico especifico introduzca el número. (0/6)")   
    data["weekday"] = input("dias de la semana: ") or ("")
    sleep(0.5)
    print("Quieres almacenar el log de transacciones en la ruta /log?(Y/N)")
    data["log"]= input()
    if data["log"] == "y" or data["log"] == "Y":
        data["log"]=input("Indica la ruta del log: ")
    else:
        data["log"]=NULL
    validar(data)
    comprobar(data)
    return(data)

def validar(data):
    if "" in data.values():
        print("No has introducido todos los datos necesarios")
        sys.exit(1)

def comprobar(data):
    print("Esto son los datos que desea introducir:")
    for x in data:
        valor = data.get(x)
        print(x," --> ",valor)
    comprobar=input("¿Ésta de acuerdo (Y/N)?:")
    if comprobar == "y" or comprobar == "Y":
        print("Realizamos inserción")
    else:
        print("No realizamos inserción")
        sys.exit(1)

data = introducirssh()
    
