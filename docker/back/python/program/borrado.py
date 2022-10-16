import conexionbbdd as bbdd
import sys
import crontab as cr
datos=bbdd.consultarParaborrados()
print("Servicios en uso:")
print("id ------------ origen ------------ final ------------ IP ------------ user")
for data in datos:
    print(str(data["ID"])+" --- "+str(data["SOURCE"])+" --- "+str(data["FINAL"])+" --- "+(data["IP"])+" --- "+(data["USER"]))
# Preguntar el id de los datos que se desean borrar 
id_borrar=  input("Indica el id del servicio de backups que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")
if id_borrar == "0":
    sys.exit(1)
else:
    ssh_borrar=bbdd.consultaridssh(id_borrar)
    print("Vamos a borrar el los datos relacionados con el id: "+id_borrar)
    bbdd.borrarSHARE(id_borrar)
    ssh_borrar= input("¿Desea borrar tambien los datos relacionados con el la conexión ss al servidor?(Y/N) ") or ("")
    if ssh_borrar == "y" or ssh_borrar == "Y":        
        bbdd.borrarSSH(ssh_borrar)
    # Realizamos borrado en crontab y vuelta a su escritura
    cr.borrar_Crontab()
    cr.todos_crontab()
    print("Finalizado la operación de borrado")

