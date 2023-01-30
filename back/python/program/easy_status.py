import conexionbbdd
import sys
try:
    status= str(sys.argv[1])
    id= str(sys.argv[2])
except:
    print("Es necesario incluir todos los parametros")
    sys.exit(1)


conexionbbdd.update_status(status,id)