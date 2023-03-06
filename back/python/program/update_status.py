import connect_db as cdb
import sys
try:
    status= str(sys.argv[1])
    id= str(sys.argv[2])
except:
    print("Es necesario incluir todos los parametros")
    sys.exit(1)

db=cdb.DataBase()
if db.check_id_exists_from_share(id) == 1:
    print("Servicio no almacenado en el sistema: "+str(id))
    sys.exit(1)
db.update_status(status,id)