FROM ubuntu
MAINTAINER IgnacioGovantes "ignaciogovo@gmail.com"

# Actualizamos
RUN apt-get update

# Instalamos python y sus paquetes
RUN apt-get install -y python3
RUN apt-get install -y python3-pip
RUN mkdir /python
COPY python/requirements.txt /python/requirements.txt
RUN pip install -r /python/requirements.txt

#el siguiente ARG desactiva las preguntas que normalmente se hacen sobre la ubicación y la zona horaria para Apache
ARG DEBIAN_FRONTEND=noninteractive

# Instalamos apache
RUN apt-get install -y apache2
# Asignamos un host valido al contenedor:
RUN echo 'ServerName 127.0.0.1' >> /etc/apache2/apache2.conf

# Instalamos mysql
RUN apt-get update 
RUN apt-get -y install mysql-server

# Instalamos cron
RUN apt-get update && apt-get install -y cron

# Instalamos suervisor
RUN apt-get install -y supervisor \
# Borramos líneas añadidas con todos los apt-get updates hechos anteriormente 
    && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /var/log/supervisor
COPY supervisor/supervisord.conf /etc/supervisor/supervisord.conf

# Indica los puertos TCP/IP los cuales se pueden accede a los servicios del contenedor
# Apache
EXPOSE 80
ADD ["apache/","/var/www/html/"]
# mysql
EXPOSE 3306

# Indicamos los volumenes compartidos:
VOLUME [ "/source" ]
# Establecemos el comando del proceso de inicio del contenedor
CMD [ "supervisord", "-c", "/etc/supervisor/supervisord.conf" ]

