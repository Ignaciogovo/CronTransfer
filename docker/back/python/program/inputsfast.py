from pydoc import importfile
import ingresos
import conexionbbdd
import crontab
import sys


try:
    id_conexion= str(sys.argv[1])
    hora= str(sys.argv[2])
    origen= str(sys.argv[3])
    final= str(sys.argv[4])
except:
    print("Es necesario incluir todos los argumentos")
    sys.exit(1)


print("Id_conexión: "+id_conexion)
print("hora: "+hora)
print("origen: "+origen)
print("final: "+final)