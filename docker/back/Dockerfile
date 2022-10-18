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

#Instalamos nano
RUN apt-get install -y nano

# Instalamos cron
RUN apt-get update && apt-get install -y cron
RUN echo "#EASYBACKUPS" >> /etc/crontab
# Instalamos suervisor
RUN apt-get install -y supervisor \
# Borramos líneas añadidas con todos los apt-get updates hechos anteriormente 
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/supervisor
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# Generamos alias para la comodidad del programa:
RUN echo 'alias hi="echo "Bienvenido a EASYBACKUPS""' >> ~/.bashrc
RUN echo 'alias IngresoCompleto="python3 /python/program/inputs.py 2"' >> ~/.bashrc
RUN echo 'alias IngresoConexion="python3 /python/program/inputs.py 1"' >> ~/.bashrc
RUN echo 'alias BorrarServicio="python3 /python/program/borrado.py"' >> ~/.bashrc
RUN echo 'alias ConsultarConexiones="python3 /python/program/conexionbbdd.py 1"' >> ~/.bashrc
RUN echo 'alias ConsultarServicios="python3 /python/program/conexionbbdd.py 2"' >> ~/.bashrc
RUN echo 'alias ConsultarDatos="python3 /python/program/conexionbbdd.py 3"' >> ~/.bashrc
RUN echo 'backupDiario="python3 /python/program/inputsfast.py"' >> ~/.bashrc


# Indicamos los volumenes compartidos:
VOLUME [ "/source" ]
# Establecemos el comando del proceso de inicio del contenedor
CMD [ "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]