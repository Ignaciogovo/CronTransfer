import crontabs
import sys
import connect_db as cdb




try:
    db=cdb.DataBase()
    id_conexion= str(sys.argv[1])
    hora= str(sys.argv[2])
    transferencia=str(sys.argv[3])
    transferencia=transferencia.lower()
    local= str(sys.argv[4])
    remoto= str(sys.argv[5])
    log = str(sys.argv[6]) or ("NULL")

except:
    print("Es necesario incluir todos los parametros")
    print("parametros: backup_daily id_conexion hora /ruta/local /ruta/remoto log(Y/N) sobrescribir(Y/N) ")
    sys.exit(1)
# Modificaciones de los datos antes del input
if log.lower() == "y":
    idshare =int(db.ultimoidSHARE())+1
    borred_share=int(db.select_deleted_id_share())+1
    if idshare < borred_share:
        idshare=borred_share
    log="/log/servicio_"+str(idshare)+"hora_"+hora+".log"
else:
    log="NULL"
sobrescribir = str(sys.argv[7]) or ("N")
if sobrescribir.lower() =="n":
    sobrescribir="N"
else:
    sobrescribir="Y"

if int(hora) not in range(0,24):
    print("La hora no es válida")
    sys.exit(1)
if transferencia != "e" and transferencia != "i":
    print("Tipo de transferencia errónea, deben ser i (importar) o e (exportar)")
    sys.exit(1)

data= {
"TRANSFERENCIA": transferencia,
"local": local,
"remoto": remoto,
"crontab" : "0 "+hora+" * * * ",
"id_conexion" : id_conexion,
"log": log,
"SOBRESCRIBIR": sobrescribir
}
## Modificamos los datos de ruta para evitar errores
if data["local"].endswith("/"):
    data["local"]=data["local"][:-1]
# Incluimos el directorio del contenedor para evitar errores
if data["local"].startswith("/"):
    data["local"]='/source'+data["local"]
else:
    data["local"]='/source'+"/"+data["local"]

# configuramos los datos proporcionados
# Eliminamos el / final para evitar errores
if data["remoto"].endswith("/"):
    data["remoto"]=data["remoto"][:-1]


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

