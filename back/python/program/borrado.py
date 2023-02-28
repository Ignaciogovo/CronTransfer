import connect_db as cdb
import sys
import f_crontabs as cr
import f_consultas as f_c
import os

def delete_file(archivo):
    try:
        os.remove(archivo)
        print("Archivo log "+archivo+" borrado exitosamente.")
    except OSError as e:
        print("Error al borrar el archivo log "+archivo+": "+e)



def borrar_servicio():
    db=cdb.DataBase()
    cerrar=f_c.c_servicio()
    if cerrar == 1:
        sys.exit(1)

    # Preguntar el id de los datos que se desean borrar 
    id_borrar=  input("Indica el id del servicio de transferencias que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")
    try:
        int(id_borrar)
    except: 
        print("Valor incorrecto")
        sys.exit()
    if str(id_borrar) == "0":
        sys.exit(1)
    else:
        if db.check_id_exists_from_share(id_borrar) == 1:
            print("Servicio no almacenado en el sistema")
            sys.exit()
        ssh_borrar=db.select_id_conexion_fromshare(id_borrar)
        log = db.select_log(id_borrar)
        print("Vamos a borrar el los datos relacionados con el id: "+id_borrar)
        db.delete_share(id_borrar)
        if log is not None:
            if input("¿Desea borrar el archivo log "+str(log)+" relacionado con el servicio?(Y/N) ").lower() == "y":
                delete_file(log)
        if input("¿Desea borrar tambien los datos relacionados con el la conexión ssh al servidor?(Y/N) ").lower() == "y":        
            db.delete_ssh(ssh_borrar)
        # Realizamos borrado en crontab y vuelta a su escritura
        cr.borrar_Crontab()
        cr.todos_crontab()
        print("Finalizado la operación de borrado")





def borrar_conexion():
    db=cdb.DataBase()
    cerrar=f_c.c_ssh()
    if cerrar == 1:
        sys.exit(1)
    # Preguntar el id de los datos que se desean borrar 
    id_borrar=  input("Indica el id de la conexión que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")
    try:
        int(id_borrar)
    except: 
        print("Valor incorrecto")
        sys.exit()
    if str(id_borrar) == "0":
        sys.exit(1)
    else:
        if db.check_id_exists_from_conexion(id_borrar) == 1:
            print("Conexión no almacenada en el sistema")
            sys.exit(1)            
        lista=db.select_id_from_share_where_id_conexion(id_borrar)
        if lista == 0:
            db.delete_ssh(id_borrar)
        else:
            if input("¿Borrar una conexión borrará todos los servicios relacionados con él, está ¿seguro?(Y/N) ").lower() == "y":
                # Borramos todos los servicios relacionados con la conexión:
                for row in lista:
                    fast_borrar_servicio(row) 
                db.delete_ssh(id_borrar)
                cr.borrar_Crontab()
                cr.todos_crontab()
                print("Finalizado la operación de borrado")
            else:
                print("No se borra la conexión: "+str(id_borrar))

def fast_borrar_servicio(id_borrar):
    try:
        int(id_borrar)
    except: 
        print("Parametro incorrecto")
        sys.exit()
    db=cdb.DataBase()
    try:
        if db.check_id_exists_from_share(id_borrar) == 1:
            print("Servicio no almacenado en el sistema")
            sys.exit()
        db.delete_share(id_borrar)
        # Realizamos borrado en crontab y vuelta a su escritura
        cr.borrar_Crontab()
        cr.todos_crontab()
        print("Finalizado la operación de borrado")
    except:
        print("No se ha podido borrar el servicio")

def fast_borrar_conexion(id_borrar):
    try:
        int(id_borrar)
    except: 
        print("Parametro incorrecto")
        sys.exit()
    db=cdb.DataBase()
    if db.check_id_exists_from_conexion(id_borrar) == 1:
        print("Conexión no almacenada en el sistema")
        sys.exit(1)
    try:
        lista=db.select_id_from_share_where_id_conexion(id_borrar)
        if lista == 0:
            db.delete_ssh(id_borrar)
        if  input("¿Borrar una conexión borrará todos los servicios relacionados con él, ¿está seguro?(Y/N) ").lower() == "y":
            for row in lista:
                fast_borrar_servicio(row)
            db.delete_share_conexion(id_borrar)       
            db.delete_ssh(id_borrar)
            cr.borrar_Crontab()
            cr.todos_crontab()
            print("Finalizado la operación de borrado")
        else:
            print("No se borra la conexión: "+str(id_borrar))
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

