import crontabs
import sys
import connect_db as cdb




try:
    db=cdb.DataBase()
    id_conexion= str(sys.argv[1])
    hora= str(sys.argv[2])
    transferencia=str(sys.argv[3])
    transferencia=transferencia.lower()
    origen= str(sys.argv[4])
    final= str(sys.argv[5])
    log = str(sys.argv[6]) or ("NULL")
    if log == "y" or log == "Y":
        idshare =int(db.ultimoidSHARE())+1
        log="/log/servicio_"+str(idshare)+"hora_"+hora+".log"
    else:
        log="NULL"
    sobrescribir = str(sys.argv[7]) or ("N")
    if sobrescribir == "N" or sobrescribir =="n":
        sobrescribir="N"
    else:
        sobrescribir="Y"
except:
    print("Es necesario incluir todos los parametros")
    print("parametros: backup_daily id_conexion hora /ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N) ")
    sys.exit(1)
if int(hora) not in range(0,24):
    print("La hora no es válida")
    sys.exit(1)
if transferencia != "e" and transferencia != "i":
    print("Tipo de transferencia errónea, deben ser i (importar) o e (exportar)")
    sys.exit(1)

data= {
"TRANSFERENCIA": transferencia,
"SOURCE": origen,
"FINAL": final,
"crontab" : "0 "+hora+" * * * ",
"id_conexion" : id_conexion,
"log": log,
"SOBRESCRIBIR": sobrescribir
}
## Modificamos los datos de ruta para evitar errores
if data["SOURCE"].endswith("/"):
    data["SOURCE"]=data["SOURCE"][:-1]
# Incluimos el directorio del contenedor para evitar errores
if data["TRANSFERENCIA"]=="e":
    if data["SOURCE"].startswith("/"):
        data["SOURCE"]='/source'+data["SOURCE"]
    else:
        data["SOURCE"]='/source'+"/"+data["SOURCE"]

# configuramos los datos proporcionados
# Eliminamos el / final para evitar errores
if data["FINAL"].endswith("/"):
    data["FINAL"]=data["FINAL"][:-1]
if data["TRANSFERENCIA"]=="i":
    if data["FINAL"].startswith("/"):
        data["FINAL"]='/source'+data["FINAL"]
    else:
        data["FINAL"]='/source'+"/"+data["FINAL"]

# Insertamos datos de share en su tabla
db.insert_share(data,None)
# Realizar Crontab:
idshare =db.ultimoidSHARE()
crontabs.RealizarCrontab(idshare)
if log != "NULL":
    print("Se guardado la configuración.")
    f = open(log, "x")
    f.close()
    print("La ruta del log de transacciones: "+log)

