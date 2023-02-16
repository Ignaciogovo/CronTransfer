import ingresos
import crontabs
import sys
from f_consultas import contar_logs
import re
import prueba_poo as pp

especiales = ("@reboot","@yearly","@annually","@monthly","@weekly","@daily","@midnight","@hourly")
dias_semana= ("sun","mon","tue","wed","thu","fri","sat")
meses = ("jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec")
def comprobación_crontab(crontab):
    crontab = " ".join(crontab.split())# Eliminamos los posibles dobles espacios
    if crontab in especiales:
        1==1
    else:
        list_comp= re.split(" ", crontab) # Separamos el crontab en una lista a partir de los espacios
        if len(list_comp) == 5:
            1==1
        else:
            print("Formato de crontab erroneo")
            sys.exit(1)

try:
    bd=pp.DataBase()
    id_conexion= str(sys.argv[1])
    crontab= str(sys.argv[2])
    comprobación_crontab(crontab)
    origen= str(sys.argv[3])
    final= str(sys.argv[4])
    log = str(sys.argv[5]) or ("NULL")
    if log == "y" or log == "Y":
        idshare =int(bd.ultimoidSHARE())+1
        log="/log/servicio_"+str(idshare)+".log"
    else:
        log="NULL"
    sobrescribir = str(sys.argv[6]) or ("N")
    if sobrescribir == "N" or sobrescribir =="n":
        sobrescribir="N"
    else:
        sobrescribir="Y"
except:
    print("Es necesario incluir todos los parametros")
    print("parametros: cron_crontab id_conexion crontab /ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N) ")
    sys.exit(1)

data= {
"SOURCE": origen,
"FINAL": final,
"crontab" : crontab,
"id_conexion" : id_conexion,
"log": log,
"SOBRESCRIBIR": sobrescribir
}
## Modificamos los datos de ruta para evitar errores
if data["SOURCE"].endswith("/"):
    data["SOURCE"]=data["SOURCE"][:-1]
# Incluimos el directorio del contenedor para evitar errores
if data["SOURCE"].startswith("/"):
    data["SOURCE"]='/source'+data["SOURCE"]
else:
    data["SOURCE"]='/source'+"/"+data["SOURCE"]

# configuramos los datos proporcionados
# Eliminamos el / final para evitar errores
if data["FINAL"].endswith("/"):
    data["FINAL"]=data["FINAL"][:-1]


# Insertamos datos de share en su tabla
bd.insert_share(data,None)
# Realizar Crontab:
idshare =bd.ultimoidSHARE()
crontabs.RealizarCrontab(idshare)
if log != "NULL":
    print("Se guardado la configuración.")
    f = open(log, "x")
    f.close()
    print("La ruta del log de transacciones: "+log)







# Conceptos crontab:


# https://www.hostinger.es/tutoriales/cron-job

# https://crontab.guru/ 


# https://geekflare.com/es/crontab-linux-with-real-time-examples-and-tools/