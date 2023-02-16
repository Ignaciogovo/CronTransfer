import prueba_poo as pp
import sys
import crontabs as cr
import f_consultas as f_c


def borrar_servicio():
    db=pp.DataBase
    cerrar=f_c.c_servicio()
    if cerrar == 1:
        sys.exit(1)

    # Preguntar el id de los datos que se desean borrar 
    id_borrar=  input("Indica el id del servicio de backups que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")
    if id_borrar == "0":
        sys.exit(1)
    else:
        ssh_borrar=db.select_share_id_conexion(id_borrar)
        print("Vamos a borrar el los datos relacionados con el id: "+id_borrar)
        db.delete_share(id_borrar)
        ssh_borrar= input("¿Desea borrar tambien los datos relacionados con el la conexión ss al servidor?(Y/N) ") or ("")
        if ssh_borrar == "y" or ssh_borrar == "Y":        
            db.delete_ssh(ssh_borrar)
        # Realizamos borrado en crontab y vuelta a su escritura
        cr.borrar_Crontab()
        cr.todos_crontab()
        print("Finalizado la operación de borrado")





def borrar_conexion():
    db=pp.DataBase
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
            db.delete_share_conexion(id_borrar)       
            db.delete_ssh(id_borrar)
            cr.borrar_Crontab()
            cr.todos_crontab()
            print("Finalizado la operación de borrado")

def fast_borrar_servicio(id_borrar):
    db=pp.DataBase
    try:
        db.delete_share(id_borrar)
        # Realizamos borrado en crontab y vuelta a su escritura
        cr.borrar_Crontab()
        cr.todos_crontab()
        print("Finalizado la operación de borrado")
    except:
        print("No se ha podido borrar el servicio")

def fast_borrar_conexion(id_borrar):
    db=pp.DataBase
    try:
            db.delete_share_conexion(id_borrar)       
            db.delete_ssh(id_borrar)
            cr.borrar_Crontab()
            cr.todos_crontab()
            print("Finalizado la operación de borrado")
    except:
        print("No se ha podido borrar la conexión")






try:
    menu= sys.argv[1]
except:
    print("Es necesario incluir un argumento")
    sys.exit(1)

if menu == "s":
    borrar_servicio()

elif menu =="c":
    borrar_conexion()
elif menu =="sf":
    try:
        id_borrar=sys.argv[2]
    except:
         print("Es necesario incluir el id del servicio")
         sys.exit(1)
    fast_borrar_servicio(id_borrar)
elif menu =="cf":
    try:
        id_borrar=sys.argv[2]
    except:
         print("Es necesario incluir el id de la conexión")
         sys.exit(1)
    fast_borrar_conexion(id_borrar)
else:
    print("No se reconoce los parametros")

