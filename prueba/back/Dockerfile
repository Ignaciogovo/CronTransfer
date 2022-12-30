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
RUN python3 /python/program/instalar_clave.py

# Creamos una carpeta para los logs de transacciones del backup
RUN mkdir /log
#Instalamos nano
RUN apt-get install -y nano

# Instalamos cron
RUN apt-get update && apt-get install -y cron
RUN echo "#EASYBACKUPS" >> /etc/crontab
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
RUN echo 'alias easy_insert="python3 /python/program/inputs.py"' >> ~/.bashrc   
RUN echo 'alias easy_insert="python3 /python/program/inputs.py "' >> ~/.bashrc 
# En este alias se añade un parametro con varias opciones(c/s/a)
RUN echo 'alias easy_delete="python3 /python/program/borrado.py"' >> ~/.bashrc
# En este alias se añade un parametro con varias opciones(c/s/a)
RUN echo 'alias easy_select="python3 /python/program/consultas.py"' >> ~/.bashrc

    # En este alias hay que añadir 4 parametros: backupDiario id_conexión hora ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N) 
RUN echo 'alias backup_daily="python3 /python/program/inputsfast.py"' >> ~/.bashrc 
RUN echo 'alias easy_crontab="python3 /python/program/inputcrontab.py"' >> ~/.bashrc 
# Incluir el parametro del id del servicio
RUN echo 'alias easy_run="python3 /python/program/compartir.py"' >> ~/.bashrc 

# Mostrar el archivo ayuda
RUN echo 'alias easy_help="cat /.textos/help.txt"' >> ~/.bashrc 

# Indicamos los volumenes compartidos:
VOLUME [ "/source" ]
# Establecemos el comando del proceso de inicio del contenedor
CMD [ "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]