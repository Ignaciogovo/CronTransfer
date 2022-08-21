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
idssh=conexionbbdd.ultimoidssh()
datosshare=ingresos.introducirshare()
# Añadimos el id del usuario de ssh a los datos de conexión
datosshare["id_conexion"]=idssh
# Insertamos datos de share en su tabla
conexionbbdd.ingresarShare(datosshare,1)
# conexionbbdd.ingresarShare(datosshare,None)
# Realizar Crontab:
idshare =conexionbbdd.ultimoidSHARE()
crontab.RealizarCrontab(idshare)