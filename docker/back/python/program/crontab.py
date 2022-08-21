from pymysql import NULL
import conexionbbdd as bbdd
import sys
def pasarbbddAcrontab(id):
    datos = bbdd.consultarDatosshare(id)
    data= {
    "minutes" : datos[0],
    "hours" : datos[1],
    "days" : datos[2],    
    "months" : datos[3],
    "weekday" : datos[4],
    "command" : str(id),
     "log": datos[5]
    }
    return(data)





def DefinirCrontab(data):
    # datos: minutos horas dias meses DiasDeSemana(weekday) archivo.py peticion log:
    crontab = data["minutes"]+" "+data["hours"]+" "+data["days"]+" "+data["months"]+" "+data["weekday"]+" root "+"python3 compartir.py"+data["id"]
    if data["log"] is not NULL:
        crontab=crontab+" >> " + data["log"]
    return(crontab)

def CrearCrontab(crontab):
    archivoCrontab = open("/etc/crontab","a")
    archivoCrontab.write(crontab)
    archivoCrontab.close()
    # PRUEBA crontab

def RealizarCrontab(id):
    data = pasarbbddAcrontab(id)
    crontab = DefinirCrontab(data)
    try:
        CrearCrontab(crontab)
    except:
        print("Se ha intentado realizar la escritura de crontab pero algo ha fallado")
        sys.exit(1)       


