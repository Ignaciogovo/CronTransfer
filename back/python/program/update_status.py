import prueba_poo as pp
import sys
try:
    status= str(sys.argv[1])
    id= str(sys.argv[2])
except:
    print("Es necesario incluir todos los parametros")
    sys.exit(1)

bd=pp.DataBase
bd.update_status(status,id)