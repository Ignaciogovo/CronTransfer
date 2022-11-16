from pydoc import importfile
import ingresos
import conexionbbdd
import crontabs
import sys
from f_consultas import contar_logs




try:
    id_conexion= str(sys.argv[1])
    hora= str(sys.argv[2])
    origen= str(sys.argv[3])
    final= str(sys.argv[4])
    log = str(sys.argv[5]) or ("NULL")
    if log == "y" or log == "Y":
        total=str(contar_logs()+1)
        log="/log/conexion_"+id_conexion+"hora_"+hora+"_"+total+".log"
    else:
        log="NULL"
    sobrescribir = str(sys.argv[6]) or ("N")
    if sobrescribir == "N" or sobrescribir =="n":
        sobrescribir="N"
    else:
        sobrescribir="Y"
except:
    print("Es necesario incluir todos los argumentos")
    sys.exit(1)

data= {
"SOURCE": origen,
"FINAL": final,
"minutes" : "0",
"hours" : hora,
"days" : "*",
"months" : "*",
"weekday" : "*",
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
conexionbbdd.ingresarShare(data,None)
# conexionbbdd.ingresarShare(datosshare,None)
# Realizar Crontab:
idshare =conexionbbdd.ultimoidSHARE()
crontabs.RealizarCrontab(idshare)
if log != "NULL":
    print("Se guardado la configuración.")
    f = open(log, "x")
    f.close()
    print("La ruta del log de transacciones: "+log)

