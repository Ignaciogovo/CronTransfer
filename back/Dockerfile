FROM ubuntu
MAINTAINER IgnacioGovantes "ignaciogovo@gmail.com"

# Actualizamos
RUN apt-get update

# Instalamos python y sus paquetes
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN mkdir /python
COPY python/ /python/
RUN pip install -r /python/requirements.txt

# introducimos la clave para el cifrado de contraseñas
RUN mkdir /.claves
###RUN python3 /python/program/instalar_clave.py

# Creamos una carpeta para los logs de transacciones del backup
RUN mkdir /log
#Instalamos nano
RUN apt-get install -y nano
# Indicamos variables de entorno:
ENV TZ Europe/Madrid
ENV MYSQL_USER python
ENV MYSQL_PASSWORD python
    # Al instalar tzdata permite seleccionar la zona horaria correcta en un menú. 
    #Esto no es útil al crear contenedores Docker por eso esta variable
ENV DEBIAN_FRONTEND noninteractive 


# Instalamos tzdata
RUN apt-get update && apt-get install -y tzdata

# Instalamos cron
RUN apt-get update && apt-get install -y cron

RUN echo "#CronTransfer" >> /etc/crontab
# Instalamos suervisor
RUN apt-get install -y supervisor \
# Borramos líneas añadidas con todos los apt-get updates hechos anteriormente 
    && rm -rf /var/lib/apt/lists/*
# /modificamos las rutas del supervisor
RUN mkdir -p /var/log/supervisor
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# Incluimos textos:
RUN mkdir ./textos
COPY textos/ /.textos/

# Generamos alias para la comodidad del programa:
RUN echo 'alias hi="cat /.textos/bienvenida.txt"' >> ~/.bashrc
RUN echo 'alias cron_insert="python3 /python/program/inputs.py"' >> ~/.bashrc   
# En este alias se añade un parametro con varias opciones(c/s/a)
RUN echo 'alias cron_delete="python3 /python/program/borrado.py"' >> ~/.bashrc
# En este alias se añade un parametro con varias opciones(c/s/a)
RUN echo 'alias cron_select="python3 /python/program/consultas.py"' >> ~/.bashrc

    # En este alias hay que añadir 4 parametros: backup_daily id_conexión hora ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N) 
RUN echo 'alias cron_daily="python3 /python/program/inputsfast.py"' >> ~/.bashrc

# Incluir el parametro del id del servicio
RUN echo 'alias cron_run="python3 /python/program/compartir.py a"' >> ~/.bashrc 

# Actualizar status
RUN echo 'alias cron_stop="python3 /python/program/update_status.py stop"' >> ~/.bashrc
RUN echo 'alias cron_activate="python3 /python/program/update_status.py activate"' >> ~/.bashrc

# Mostrar el archivo ayuda
RUN echo 'alias cron_help="cat /.textos/help.txt"' >> ~/.bashrc 

# Indicamos los volumenes compartidos:
VOLUME [ "/source" ]

# copiamos el archivo para ejecutar al inicio del servidor
COPY start.sh /start.sh
RUN chmod +x /start.sh

# Establecemos el comando del proceso de inicio del contenedor
CMD ["/start.sh"]
# CMD [ "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]