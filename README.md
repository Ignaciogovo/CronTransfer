# Easybackups
<p align="center">
  <a href="#objetivo">Objetivo</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#formas-de-uso">Formas de uso</a> •
  <a href="#metas-del-proyecto">Metas del proyecto</a><br>
</p>

## Objetivo

`Easybackups` es un proyecto pensado para facilitar las copias de seguridad recurrentes de archivos o directorios entre servidores.
Las conexiones entre estos servidores se producen por ssh, además usamos otras tecnologías como python o docker.


## Instalación

### Dos formas de instalación:
- 1 Instalación desde los archivos dockerfile
- 2 Instalación con las imagenes incluidas en docker hub

#### 1 Instalación desde los archivos dockerfile

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



## Formas de uso
Accedemos al contenedor docker:
```bash
> docker exec -it program /bin/bash
```

### Mostrar por pantalla todos los comandos
```bash
> easy_help
```

### Inserción servicio con guía
Realizar una inserción de servicio completo (Por defecto): (Se ejecuta una guía para facilitar insercción)
```bash
> easy_insert s 
```
  --> Es necesario poner la ruta absoluta en las rutas origen y final.

### Inserción conexión con guía
Realizar una inserción de datos de un servidor remoto:
```bash
> easy_insert c
```
### Inserción rapída de conexión 
Realizar una inserción de datos de un servidor remoto:
  Parametros: IP, puerto(d='Por defecto'/ cualquier puerto) usuario p/k --> password/key
```bash
> easy_insert cf 192.168.1.4 d  usuario p 
  Introduzca la contraseña:
```


  




### Inserción rápida de serivicios
Realizar una inserción rápida de servicio backup diario
  Parametros: id_conexion hora /ruta/origen /ruta/final log(Y/N) sobrescribir(Y/N)
Ejemplo
```bash
> backup_daily 7 3 /backups_bbdd/ultimobackup.sql /backups Y N
```
--Se enviaría el archivo /backups_bbdd/ultimobackup.sql a la ruta /backups de la conexión con id 7 todos los días a las 3 AM con archivo log 
  y sin sobrescribir la backup en el servidor remoto.                     
  --> Es necesario poner la ruta absoluta en las rutas origen y final.


### Consultas
Consultar conexiones: 
```bash
> easy_select c
```

Consultar servicios:
```bash
> easy_select s
```
Consultar todo (Por defecto):
```bash
> easy_select a
```


### Ejecutar un servicio en el momento:
  Parametro: número del id del servicio
```bash
> easy_run id
```
  Ejemplo: easy_run 7 --> Se ejecuta el servicio con id 7

### Borrar con guía:

Borrar servicios
```bash
> easy_delete s
```
Borrar conexión
```bash
> easy_delete c
```
con esta opción se borrarán todos los servicios vinculados a la conexión


#### Borrar con parametros
Borrar servicios
  Parametro: id del servicio
```bash
> easy_delete sf id
```
Borrar conexión
  Parametro: id de la conexión
```bash
> easy_delete cf id
```

## Metas del proyecto
- Realizar una interfaz web
- Incluir conexiones con almacenamiento en la nube
- Optimizar código
- Añadir Ingles y otros idiomas
