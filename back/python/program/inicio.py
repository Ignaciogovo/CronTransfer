from cifradopass import genera_clave
import os
genera_clave()


user = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")



with open('/etc/crontab', 'r+') as file:
    # Mueve el puntero del archivo a la posición 5
    file.seek(6)

    # Escribe el texto 'nuevo texto' en esa posición
    file.write('MYSQL_USER='+user)
    file.write('MYSQL_PASSWORD='+password)
    
    # Lee el contenido completo del archivo
    content = file.read()
    