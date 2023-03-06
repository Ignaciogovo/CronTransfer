# CronTransfer
<p align="center">
  <a href="#objetivo">Objetivo</a> •
  <a href="#instalación">Instalación</a> •
  <a href="#formas-de-uso">Formas de uso</a> •
  <a href="#Comentarios">Comentarios</a> •
  <a href="#metas-del-proyecto">Metas del proyecto</a><br>
</p>

## Objetivo

Crontransfer es un proyecto desarrollado en Python que utiliza tecnologías como Docker y MySQL para administrar y realizar transferencias programadas a otros servidores a través de SSH. Este programa permite automatizar procesos de transferencia de archivos desde un servidor a otro, y se programa en base a un horario específico en formato cron. La información necesaria para realizar las transferencias, como el horario, el servidor de origen y destino, y los archivos a transferir, se almacena en una base de datos MySQL, permitiendo una gestión centralizada y eficiente de todas las transferencias programadas. Con Crontransfer, se puede ahorrar tiempo en la gestión manual de transferencias y asegurar la seguridad de los datos transferidos mediante el uso de SSH.


## Instalación

### Dos formas de instalación:
- 1 Instalación desde los archivos dockerfile
- 2 Instalación con las imagenes incluidas en docker hub

#### 1 Instalación desde los archivos dockerfile

Clonamos el repositorio
```bash
> git clone https://github.com/Ignaciogovo/CronTransfer.git
```

Accedemos a directorio back para crear la primera imagen 
```bash
> cd back
```
Creamos la imagen cronbapp:1.0
```bash
> docker build -t cronbapp:1.0 .
```

Accedemos al directorio bbdd para crear la segunda imagen
```bash
> cd ../bbdd
```
Creamos la imagen cronbmysql:1.0
```bash
> docker build -t cronbmysql:1.0 .
```

Volvemos al direcorio principial
```bash
> cd ../bbdd
```

Ejecutamos el docker-compose
```bash
> docker-compose up -d
```

#### Instalación con las imagenes incluidas en docker hub
Ejecutar el archivo docker-compose: <a href="/recursos/CronTransfer/docker-compose.yml">docker-compose.yml</a> con sus respectivas modificaciones

## Formas de uso
Accedemos al contenedor docker:
```bash
> docker exec -it program /bin/bash
```

### Mostrar por pantalla todos los comandos
```bash
> cron_help
```

### Inserción servicio con guía
Realizar una inserción de servicio completo (Por defecto): (Se ejecuta una guía para facilitar insercción)
```bash
> cron_insert s 
```
--> Es necesario poner la ruta absoluta en las rutas local y remoto. En el caso de modificar la dirección del archivo compartido source en el docker-compose: <a href="#directorio-source-del-contenedor-program">Comentarios</a>

### Inserción conexión con guía
Realizar una inserción de datos de un servidor remoto:
```bash
> cron_insert c
```
### Inserción con parametros de conexión 
Realizar una inserción de datos de un servidor remoto:
  Parametros: IP, puerto(d='Por defecto'/ cualquier puerto) usuario p/k --> password/key
```bash
> cron_insert cf 192.168.1.4 d  usuario p 
  Introduzca la contraseña:
```
 <a href="/examples/examples_insert.txt">Ejemplos cron_insert cf</a>

### Inserción con parametros de servicio con formato crontab
Insertar de forma rápida el codigo en formato crontab:
 Parametros: id_conexion formato_crontab importar/exportar(i/e) /ruta/local /ruta/remoto log(Y/N) sobrescribir(Y/N)
```bash
> cron_insert sf 1  " * * * * 4-6 " i /backups/ultimobackup.sql /backups_bbdd Y Y
```
 <a href="/examples/examples_insert.txt">Ejemplos cron_insert sf</a>, <a href="/examples/example_cron.txt">Ejemplos horario cron</a>

--> Es necesario poner la ruta absoluta en las rutas local y remoto. Si se cambia dirección del archivo compartido source: <a href="#directorio-source-del-contenedor-program">Comentarios</a>

  




### Inserción rápida de servicios
#### cron_daily
Realizar una inserción rápida de servicio transferencia diaria
  Parametros: id_conexion hora importar/exportar(i/e) /ruta/local /ruta/remoto log(Y/N) sobrescribir(Y/N)
Ejemplo
```bash
> cron_daily 7 3 e /backups_bbdd/ultimobackup.sql /backups Y N
```
--Se enviaría el archivo /backups_bbdd/ultimobackup.sql a la ruta /backups de la conexión con id 7 todos los días a las 3 AM con archivo log 
  y sin sobrescribir la backup en el servidor remoto.                     
  <a href="/examples/examples_insert.txt">Ejemplos cron_daily</a>
  
  --> Es necesario poner la ruta absoluta en las rutas local y remoto. En el caso de modificar la dirección del archivo compartido source en el docker-compose: <a href="#directorio-source-del-contenedor-program">Comentarios</a>

### Consultas
Consultar conexiones: 
```bash
> cron_select c
```

Consultar servicios:
```bash
> cron_select s
```
Consultar todo (Por defecto):
```bash
> cron_select a
```

### Parar y activar el servicio:
Parar servicio
```bash
> cron_stop id
```
Activar servicio:
```bash
> cron_activate id
```

### Ejecutar un servicio en el momento:
  Parametro: número del id del servicio
```bash
> cron_run id
```
  Ejemplo: cron_run 7 --> Se ejecuta el servicio con id 7
 
 Si el servicio esta apagado:
 forzar ejecución
  Ejemplo: cron_run 7 f

### Borrar con guía:

Borrar servicios
```bash
> cron_delete s
```
Borrar conexión
```bash
> cron_delete c
```
con esta opción se borrarán todos los servicios vinculados a la conexión


### Borrar con parametros
Borrar servicios
  Parametro: id del servicio
```bash
> cron_delete sf id
```
Borrar conexión
  Parametro: id de la conexión
```bash
> cron_delete cf id
```


## Comentarios
### Directorio /source del contenedor program
Se requiere un directorio compartido con la máquina local, este directorio es llamado "source".
Todos los archivos necesarios deben estar en este directorio(clave privada, archivos que se desea transferir o directorios finales).
No es necesario incluir "/source/" en la ruta del archivo ya que el programa lo añade automáticamente al buscar archivos en la carpeta compartida.
Por lo tanto, si un usuario tiene un archivo en la ruta absoluta "/home/usuario/archivo.txt" y la configuración del archivo compartido es "/home/usuario:/source" el programa puede acceder a él utilizando la ruta "/archivo.txt" en lugar de "/source/archivo.txt".
  
### Servidor remoto
Para usar la versión 0.5 del programa, el servidor remoto debe tener de sistema operativo Linux. 
Si quieres importar un directorio desde el servidor remoto, se debe tener instalado en el servidor uno de los clientes de terminales tar, 7z o zip. Ya que para transferir los directorios, primero hacemos una compresión del mismo. Para importar un archivo no es necesario comprimir por lo tanto se necesita el uso de estos programas.


### Rutas
Es necesario usar las rutas absolutas. En el caso de la ruta del equipo local hay que seguir los pasos del comentario: <a href="#directorio-source-del-contenedor-program">Directorio /source del contenedor program</a>. El uso de ~ en la ruta, como por ejemplo la ruta: ~/Downloads no es compatible

## Metas del proyecto
- Realizar una interfaz web
- Incluir conexiones con almacenamiento en la nube
- Optimizar código
- Dar la posibilidad de comprimir y descomprimir el direcotorio/archivo
- Incluir a windows/
- Añadir Ingles y otros idiomas
