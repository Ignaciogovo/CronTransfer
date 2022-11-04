# Easybackups
### Objetivo

`Easybackups` es un proyecto pensado para facilitar las copias de seguridad recurrentes de archivos o directorios entre servidores.
Las conexiones entre estos servidores se producen por ssh, además usamos otras tecnologías como python o docker.


### Instalación

#### Dos formas de instalación:
- 1 Instalación desde los archivos dockerfile
- 2 Instalación con las imagenes incluidas en docker hub

1 Instalación desde los archivos dockerfile

Clonamos el repositorio
```bash
> git clone https://github.com/Ignaciogovo/Easybackups.git
```

Accedemos a directorio back para crear la primera imagen 
```bash
> cd back
```
Creamos la imagen easybapp:1.0
```bash
> docker build -t easybapp:1.0 .
```

Accedemos al directorio bbdd para crear la segunda imagen
```bash
> cd ../bbdd
```
Creamos la imagen easybmysql:1.0
```bash
> docker build -t easybmysql:1.0 .
```

Volvemos al direcorio principial
```bash
> cd ../bbdd
```

Ejecutamos el docker-compose
```bash
> docker-compose up -d
```



### Formas de uso
Accedemos al contenedor docker:
```bash
> docker exec -it program /bin/bash
```

Realizar una inserción de datos de un servidor remoto:
```bash
> docker exec -it program /bin/bash
```
