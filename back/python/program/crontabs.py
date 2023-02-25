from pymysql import NULL
import connect_db as cdb
import sys

def DefinirCrontab(data):
    # datos: minutos horas dias meses DiasDeSemana(weekday) archivo.py peticion log:
    crontab = data["crontab"]+" root "+"python3 /python/program/compartir.py "
    if data["log"] ==None:
        crontab=crontab+"NULL"
    else:
        crontab=crontab+data["log"]
    crontab=crontab+" "+str(data["id"])
    crontab=crontab+"\n"
    return(crontab)

def CrearCrontab(crontab):
    archivoCrontab = open("/etc/crontab","a")
    archivoCrontab.write(crontab)
    archivoCrontab.close()

def RealizarCrontab(id):
    db=cdb.DataBase()
    data = db.select_un_servicio(id)
    crontab = DefinirCrontab(data)
    try:
        CrearCrontab(crontab)
    except:
        print("Se ha intentado realizar la escritura de crontab pero algo ha fallado")
        sys.exit(1)


def borrar_Crontab():
    # Leer archivo linea a linea
    f = open("/etc/crontab", "r")
    puntoB = 1
    for x in f:
        if "#CronTransfer" in x:
            break
        puntoB=puntoB+1
    f.close()
    with open("/etc/crontab", 'r+') as fp:
        lineas= fp.readlines()
        fp.seek(0)
        fp.truncate()
        for numeroL, linea in enumerate(lineas):
            if numeroL < (puntoB):
                fp.write(linea)
    fp.close()
    

# Con esta función insertamos todos los crontab almacenados en la base de datos
def todos_crontab():
    db=cdb.DataBase()
    datos=db.select_servicios()
    if datos !=0:
        for data in datos:
            crontab = DefinirCrontab(data)
            try:
                CrearCrontab(crontab)
            except:
                print("Se ha intentado realizar la escritura de crontab con id: "+str(data["id"])+" pero algo ha fallado")
            


