from pymysql import NULL
import conexionbbdd as bbdd
import sys

def DefinirCrontab(data):
    # datos: minutos horas dias meses DiasDeSemana(weekday) archivo.py peticion log:
    crontab = data["minutes"]+" "+data["hours"]+" "+data["days"]+" "+data["months"]+" "+data["weekday"]+" root "+"python3 /python/program/compartir.py "+data["id"]
    if data["log"] != "NULL":
        crontab=crontab+" >> " + data["log"]
    return(crontab)

def CrearCrontab(crontab):
    archivoCrontab = open("/etc/crontab","a")
    archivoCrontab.write(crontab)
    archivoCrontab.close()
    # PRUEBA crontab

def RealizarCrontab(id):
    data = bbdd.consultarDatosshare(id)
    crontab = DefinirCrontab(data)
    try:
        CrearCrontab(crontab)
    except:
        print("Se ha intentado realizar la escritura de crontab pero algo ha fallado")
        sys.exit(1)


