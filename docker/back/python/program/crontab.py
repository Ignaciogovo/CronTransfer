from pymysql import NULL


def pasarbbddAcrontab():
    print("prueba")





def DefinirCrontab(data):
    # datos: minutos horas dias meses DiasDeSemana(weekday) archivo.py peticion log:
    crontab = data["minutes"]+" "+data["hours"]+" "+data["days"]+" "+data["months"]+" "+data["weekday"]+" root "+data["command"]+" "+data["peticion"]
    if data["log"] is not NULL:
        crontab=crontab+" >> " + data["log"]
    return(crontab)

def CrearCrontab(crontab):
    archivoCrontab = open("/etc/crontab","a")
    archivoCrontab.write(crontab)
    archivoCrontab.close()
    # PRUEBA crontab
data= {
    "minutes" : "*",
    "hours" : "*",
    "days" : "*",    
    "months" : "*",
    "weekday" : "*",
    "command" : "date",
    "peticion" : str(1)
     ,"log": "/ruta/archivo.log"
}

print(DefinirCrontab(data))

