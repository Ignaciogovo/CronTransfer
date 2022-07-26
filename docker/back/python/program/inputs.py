from pydoc import importfile
import ingresos
import conexionbbdd
import crontab

# Coger datos de ssh
datosssh=ingresos.introducirssh()
# Insertar datos en la base de datos
conexionbbdd.ingresarSSH(datosssh)

# Coger datos para tabla share
# Cogemos el id del usuario que hemos escrito anteriormente
idssh=conexionbbdd.colsutaridssh()
datosshare=ingresos.introducirshare()
# Añadimos el id del usuario de ssh a los datos de conexión
datosshare["id_conexion"]=idssh
# Insertamos datos de share en su tabla
conexionbbdd.ingresarShare(datosshare)