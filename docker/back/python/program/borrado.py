import conexionbbdd as bbdd
import sys
import crontab as cr
import f_consultas as f_c


def borrar_servicio():
    cerrar=f_c.c_servicio
    if cerrar == 1:
        sys.exit(1)

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





def borrar_conexion():
    cerrar=f_c.c_ssh()
    if cerrar == 1:
        sys.exit(1)
    # Preguntar el id de los datos que se desean borrar 
    id_borrar=  input("Indica el id de la conexión que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")
    if id_borrar == "0":
        sys.exit(1)
    else:
        ssh_borrar= input("¿Borrar una conexión borrará todos los servicios relacionados con él, está ¿seguro?(Y/N) ") or ("")
        if ssh_borrar == "y" or ssh_borrar == "Y":
            # Borramos todos los servicios relacionados con la conexión:
            bbdd.borrarSHARE_conexion(id_borrar)       
            bbdd.borrarSSH(id_borrar)
            cr.borrar_Crontab()
            cr.todos_crontab()
            print("Finalizado la operación de borrado")

try:
    menu= sys.argv[1]
except:
    print("Es necesario incluir un argumento")
    sys.exit(1)
if menu == "1":
    borrar_servicio()

elif menu =="2":
    borrar_conexion()
else:
    print("No se reconoce los argumentos")


