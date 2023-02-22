from cifradopass import genera_clave
import os
import sys

tiempo= os.getenv("TZ")
user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")



with open('/etc/crontab', 'r+') as file:
    contenido = file.readlines()
    if "Variables de entorno".lower() in ''.join(contenido).lower():
        sys.exit(1)
    else:
        # Agrega el texto 'Variables de entorno' en la línea 6
        contenido.insert(5, '#Variables de entorno\n')
        # Agrega las variables MYSQL_USER y MYSQL_PASSWORD en las líneas 7 y 8
        contenido.insert(6, 'TZ=' + tiempo + '\n')
        contenido.insert(7, 'MYSQL_USER=' + user + '\n')
        contenido.insert(8, 'MYSQL_PASSWORD=' + password + '\n')
        # Vuelve al principio del archivo
        file.seek(0)
        # Escribe el contenido actualizado en el archivo
        file.writelines(contenido)
genera_clave()