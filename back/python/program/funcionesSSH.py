import paramiko
from datetime import datetime
import os
import shutil
import cifradopass as cp

class operations_transfer:
    def __init__(self,data):
        self.data=data
        self.host=data["HOST"]
        self.username=data["USER"]
        self.port=data["PORT"]
        self.client = None
        self.private_key=None
        self.password=None
        # Variable para comentar estado cuando se realiza función de connect
        self.estado=None
        
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #Seguridad:
        if self.data["TIPO"]=='clave':
            try:
                self.private_key =paramiko.RSAKey.from_private_key_file(self.data["CLAVE"])
                self.password = None

            except Exception as e:
                print("Error al cargar la clave privada:", e)
                return(1)
        else:
            self.password = cp.desencriptar_pass(self.data["PASS"])
            self.private_key = None
        try:
            if self.data["TIPO"]=='clave':
                self.client.connect(self.host, port=self.port,username=self.username, pkey=self.private_key)
            else:
                self.client.connect(self.host,port=self.port, username=self.username, password=self.password)
            return(0)
        except Exception as e:
            print("Error al conectar con el servidor: ", e)
            if self.estado != None:
                print("Fallo en "+self.estado)

            return(1)
        
    def disconnect(self):
        if self.client is not None:
            self.client.close()
    
    def check_connect(self):
        self.estado="Chequeo conexion"
        control=self.connect()
        if control==1:
            return(1)
        else:
            self.disconnect()
            return(0)
    # Chequear ruta inicial
    def check_formato_ruta(self):
        self.estado="Chequeo ruta origen"
        if self.data["TRANSFERENCIA"]=="i":
            control=self.connect()
            if control==1:
                return(1)
            try:
                # 
                ruta=self.data["SOURCE"]
                command='[ -f '+ruta+' ] && echo "archivo" || ([ -d '+ruta+' ] && echo "directorio" || echo "1")'
                stdin, stdout, stderr = self.client.exec_command(command)
                # stdin, stdout, stderr = self.client.exec_command(command)
                # Mostrar la salida del comando
                output = stdout.read().decode("utf-8")
                if output:
                    if "archivo" in output:
                        return("archivo")
                    elif "directorio" in output:
                        return("directorio")
                    else:
                        print("No se ha reconocido la ruta origen, ¿Es la ruta correcta? -->"+self.data["SOURCE"])
                        return(1)
            except Exception as e:
                print("Error al reconocer la ruta: ", e)
                return(1)
            finally:
                self.disconnect()
        else:
            if os.path.isfile(self.data["SOURCE"]):
                return("archivo")
            else:
                if os.path.isdir(self.data["SOURCE"]):
                    return("directorio")
                else:
                    print("No se ha reconocido la ruta origen, ¿Es la ruta correcta? -->"+self.data["SOURCE"])
                    return(1)


    # Chequear ruta final
    def check_ruta_final(self):
        self.estado="Chequeo ruta final"
        if self.data["TRANSFERENCIA"]=="e":
            control=self.connect()
            if control==1:
                return(1)
            try:
                # 
                ruta=self.data["FINAL"]
                command='[ -f '+ruta+' ] && echo "archivo" || ([ -d '+ruta+' ] && echo "directorio" || echo "1")'
                stdin, stdout, stderr = self.client.exec_command(command)
                # Mostrar la salida del comando
                output = stdout.read().decode("utf-8")
                if output:
                    if "archivo" in output:
                        return(1)
                    elif "directorio" in output:
                        return(0)
                    else:
                        return(1)
            except Exception as e:
                return(1)
            finally:
                self.disconnect()
        else:
            if os.path.exists(self.data["FINAL"]):
                return(0)
            else:
                return(1)
    
    # Configuracion de la ruta inicial:
    def configuracion_ruta_final(self):
        # Cogemos el nombre de los archivos
        origen=(self.data["SOURCE"])[((self.data["SOURCE"]).rfind("/")):]
        valorfinal=self.check_ruta_final()
        # Si la ruta es correcta le añadimos a la ruta el archivo origen
        if valorfinal==0:
            self.data["FINAL"]=self.data["FINAL"]+origen
            # Si la ruta es incorrecta cambiamos el dato final por el dato origen
        else:
            # Comprobamos si la ruta padre al menos es correcta
            #  Cogemos la ruta padre del archivo final
            vieja=self.data["FINAL"]
            self.data["FINAL"]=(self.data["FINAL"])[:((self.data["FINAL"]).rfind("/"))]
            valorfinal=self.check_ruta_final()
            if valorfinal==0:
                self.data["FINAL"]=self.data["FINAL"]+origen
            else:
                print("No se ha reconocido la ruta final, ¿Es la ruta correcta? -->"+vieja)
                return(1)
    # Realizar compresion
    # Solo para servidores linux
    def create_zip(self):
        self.estado="Creación zip temporal"
        if self.data["TRANSFERENCIA"]=="i":
            control=self.connect()
            if control==1:
                return(1)
            directorio=self.data["SOURCE"]
            # Probamos distintas opciones de compresion
            tipos_compresion=["zip -r ","7z a ","tar -czvf "]
            no_install=[]
            for compresion in tipos_compresion:
                # Ejecutar el comando zip en el servidor remoto a través de la conexión SSH
                command= compresion+directorio+".zip "+directorio
                stdin, stdout, stderr = self.client.exec_command(command)

                # Mostrar la salida del comando
                output = stdout.read().decode("utf-8")
                stderr = stderr.read().decode("utf-8")
                if output:
                    self.disconnect()
                    if "Permission denied" in output:
                        print("No hay permisos para realizar compresión"+output)
                        return(1)
                    else:
                        # Comprobamos si el archivo existe
                        comprobar=self.check_archivo_remoto(directorio+".zip")
                        if comprobar ==1:
                            print("Fallo al realizar compresión")
                            return(1)
                        else:
                            self.data["SOURCE"]=directorio+".zip"
                            self.data["ZIP"]="YES"
                            return(0)
                else:
                    if stderr:
                        if "command not found" in stderr:
                            no_install.append(stderr)
                            if compresion == tipos_compresion[-1]:
                                print("Fallo al realizar la compresión, se ha intentado varios metodos de compresión (zip,7z,tar)")
                                print(no_install)
                                return(1)
                        else:
                            print("Fallo al realizar la compresión: "+stderr)
                            return(1)

        else:
            archivo_zip = shutil.make_archive(self.data["SOURCE"], "zip", self.data["SOURCE"])
            # Comprobamos si se ha realizado correctamente
            if os.path.isfile(archivo_zip):
                self.data["SOURCE"]=archivo_zip
                self.data["ZIP"] = "YES"
                return(0)
            else:
                    print("Fallo al realizar compresion")
                    return(1)
    # Chequeamos el archivo de compresion
    def check_archivo_remoto(self,archivo):
        control=self.connect()
        if control==1:
            return(1)
        command='[ -f '+archivo+' ] && echo "archivo" || echo "1")'
        stdin, stdout, stderr = self.client.exec_command(command)
        # stdin, stdout, stderr = self.client.exec_command(command)
        # Mostrar la salida del comando
        output = stdout.read().decode("utf-8")
        self.disconnect()
        if output:
            if "archivo" in output:
                return("archivo")
            else:
                return(1)

    # Borrar archivo comprimido del origen
    def drop_zip(self):
        self.estado="borrado zip temporal"
        if "ZIP"in self.data and self.data["ZIP"]=="YES":
            if self.data["TRANSFERENCIA"]=="i":
                control=self.connect()
                if control==1:
                    return(1)
                ruta_zip=self.data["SOURCE"]
                sftp=self.client.open_sftp()
                try:
                    sftp.unlink(ruta_zip)
                    return(0)
                except:
                    return(2)
                finally:
                    sftp.close()
                    self.disconnect()

            else:
                try:
                # Borrar archivo zip
                    os.remove(self.data["SOURCE"])
                    return(0)
                except:
                    return(2)
        else:
            return(0)
            
    # Generamos nombre_archivo
    def generarArchivoFecha(self):
        final=(self.data["FINAL"])[((self.data["FINAL"]).rfind("/"))+1:]
        #fecha actual
        now = datetime.now()
        now= ("f_"+str(now.year)+str(now.month)+str(now.day)+"_"+str(now.hour)+str(now.minute)+"_")
        #Datetime
        now=now+final
        self.data["FINAL"]=self.data["FINAL"].replace(final,now)


    # Transferimos archivo
    def transfer_file(self):
        self.estado="Transfiriendo el archivo"
        control=self.connect()
        if control==1:
            return(1)
        try:
            sftp_client = self.client.open_sftp()
            if self.data["TRANSFERENCIA"]=="i":
                sftp_client.get(
                    self.data["SOURCE"],
                    self.data["FINAL"]
                )
            else:
                sftp_client.put(
                    self.data["SOURCE"],
                    self.data["FINAL"]
                )
            sftp_client.close()
            self.disconnect()       
            return(0)
        except Exception as e:
            print("Error al transferir el archivo: ", e)
            self.disconnect()       
            return(1)
        # Cerramos la conexión        

    






















