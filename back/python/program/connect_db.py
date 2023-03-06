# Configuración metodo poo
import pymysql
import sys
import os


class DataBase:
    def __init__(self):
        self.host = 'bbdd'
        self.user = os.getenv("MYSQL_USER")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = 'CronTransfer'
        self.charset = 'utf8mb4'
        self.conn = None
        
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host, 
                user=self.user, 
                password=self.password, 
                database=self.database, 
                charset=self.charset
            )
        except:
            print("No se puede conectar con el servidor de base de datos")
            sys.exit(1)

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
    
    # Realizar ingresos:
    def insert_ssh(self,data):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO conexionssh(IP,port,user,tipo,pass,clave) VALUES (%s,%s,%s,%s,%s,%s)"
                values=(data["HOST"],data["PORT"],data["USER"],data["TIPO"],data["PASS"],data["CLAVE"])
                cursor.execute(sql,values)
                self.conn.commit()
                print("Datos insertados correctamente.")
        except Exception as e:
            print("Error al insertar datos: ", e)
            self.conn.rollback()
        finally:
            self.disconnect()    

    def insert_share(self, data,borrar):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                # Comprobar si la clave foránea existe
                cursor.execute("SELECT * FROM conexionssh WHERE id=%s",data["id_conexion"])
                result = cursor.fetchone()
                if result is None:
                    print("La clave for  nea no existe.")
                    raise

                # Insertar datos
                sql = "INSERT INTO share(tipo_transferencia,ruta_local,ruta_remoto,id_conexion,crontab,log,sobrescribir) VALUES (%s,%s,%s,%s,%s,%s,%s)"
                values=(data["TRANSFERENCIA"],data["local"],data["remoto"],data["id_conexion"],data["crontab"],data["log"],data["SOBRESCRIBIR"])
                cursor.execute(sql,values)
                self.conn.commit()
                print("Datos insertados correctamente.")
                return(0)

        except Exception as e:
            print("Error al insertar datos: ", e)
            if borrar is not None:
                borrar=input("  Desea borrar los datos de conexi  n de ssh escritos anteriormente?(Y/N)")
                if borrar== "y" or borrar == "Y":
                    print("Borramos datos de conexi  n ssh relacionados")
                    self.delete_ssh(data["id_conexion"])
            return(1)
        finally:
            self.disconnect()

    def insert_deleted_id_share(self,id):
        try:
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO deleted_id_share(id_share) VALUES (%s)"
                values=(id)
                cursor.execute(sql,values)
                self.conn.commit()
                print("Datos insertados correctamente.")
        except Exception as e:
            print("Error al insertar datos: ", e)
            self.conn.rollback()

    # Realizar updates:
    def update_status(self,status,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "update share set `status`=%s where id=%s;"
                values=(status,id)
                cursor.execute(sql,values)
                self.conn.commit()
                print("Nuevo estado del servicio: "+status)
        except Exception as e:
            print("Error al actualizar datos: ", e)
        finally:
            self.disconnect()
    
    # Realizar deletes:
    def delete_ssh(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "delete from conexionssh where id=%s;"
                cursor.execute(sql,id)
                self.conn.commit()
        except Exception as e:
            print("Error al borrar datos: ", e)
        finally:
            self.disconnect()


    def delete_share(self,id):
        try:
            x=1
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "delete from share where id=%s;"
                cursor.execute(sql,id)
                self.conn.commit()
                x=0
        except Exception as e:
            print("Error al borrar datos: ", e)
        finally:
            if x ==0:
                self.insert_deleted_id_share(id)
            self.disconnect()




# Consultas a la base de datos

#########################################################################
# Consultas en tabla conexionssh:
########################################################################

    def check_id_exists_from_conexion(self, id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM conexionssh WHERE id = %s;"
                cursor.execute(sql, id)
                resultado = cursor.fetchone()
                return 0 if resultado[0] > 0 else 1
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()


    def ultimoidssh(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select id from conexionssh order by fecha desc;"
                cursor.execute(sql)
                resultado = cursor.fetchone()
                resultado = str(resultado[0])
                return(resultado)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

# Consultamos los datos de conexionssh de forma individual
    def select_datos_ssh(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select IP, port, user,tipo, pass,clave from conexionssh where id=%s;"
                cursor.execute(sql,id)
                datosSSH = cursor.fetchone()
                data={}
                data["HOST"]= datosSSH[0]
                data["PORT"] = datosSSH[1]
                data["USER"] = datosSSH[2]
                data["TIPO"] = datosSSH[3]
                data["PASS"] = datosSSH[4]
                data["CLAVE"] = datosSSH[5]
                return(data)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

    def select_todas_conexiones(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select id, IP,port, user, tipo,clave, fecha from conexionssh;"
                cursor.execute(sql)
                conexiones = cursor.fetchall()                
                if conexiones:
                    matriz = []
                    for row in conexiones:
                        data = {
                        "ID" : row[0],
                        "IP" : row[1],
                        "PORT" : row[2], 
                        "USER" : row[3], 
                        "TIPO": row[4],
                        "FECHA": row[5]
                        }
                        matriz.append(data)
                    return matriz
                else:
                    return 0           
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()


 #########################################################################
# Consultas en tabla share:
##########################################################################
    def check_id_exists_from_share(self, id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "SELECT COUNT(*) FROM share WHERE id = %s;"
                cursor.execute(sql, id)
                resultado = cursor.fetchone()
                return 0 if resultado[0] > 0 else 1
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

    def select_id_conexion_fromshare(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select id_conexion from share where id=%s"
                cursor.execute(sql,id)
                resultado = cursor.fetchone()
                resultado = str(resultado[0])
                return(resultado)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

    # Obtenemos todos los id a partir del id_conexión
    def select_id_from_share_where_id_conexion(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select id from share where id_conexion=%s"
                cursor.execute(sql,id)
                resultado = cursor.fetchall()
                lista=()
                if resultado:
                    for row in resultado:
                        lista.append(row[0])
                    return(lista)
                else:
                    return(0)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()
    
    def select_share_origen_final(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select tipo_transferencia,ruta_local,ruta_remoto,sobrescribir from share where id=%s;"
                cursor.execute(sql,id)
                resultado = cursor.fetchone()
                return(resultado)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

    def select_log(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select log from share where id=%s;"
                cursor.execute(sql,id)
                resultado = cursor.fetchone()
                return None if resultado[0] == 'NULL' else resultado[0]
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()
    
    def ultimoidSHARE(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select id from share order by fecha desc;"
                cursor.execute(sql)
                resultado = cursor.fetchone()
                if resultado is None:
                    return(0)
                else:
                    resultado = str(resultado[0])
                    return(resultado)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()
    
    def select_un_servicio(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select crontab, log, status from share where id=%s;"
                cursor.execute(sql,id)
                datos = cursor.fetchone()
                data= {
                "crontab" : datos[0],
                "id" : str(id),
                "log": datos[1]
                }
                return(data)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()
    
    def select_servicios(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select crontab, log, id from share;"
                cursor.execute(sql)
                datos = cursor.fetchall()
                if datos:
                    matriz= []
                    for row in datos:
                        data = {
                        "crontab" : row[0],
                        "log" : row[1],
                        "id" : row[2]
                        }
                        matriz.append(data)
                    return(matriz)
                else:
                    return(0)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

    
    def select_status(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select status from share where id = %s;"
                cursor.execute(sql,id)
                datos = cursor.fetchone()
                status=datos[0]
                return(status)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()

#########################################################################
# Consultas en tabla deleted_id_share:
########################################################################
    def select_deleted_id_share(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select max(id_share) from deleted_id_share;"
                cursor.execute(sql)
                datos = cursor.fetchone()
                deleted_id=datos[0]
                if deleted_id is not None:
                    return(deleted_id)
                else:
                    return(0)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()
#########################################################################
# Consultas en varias tablas:
#########################################################################

    def select_todo(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select  sh.id, ruta_local,ruta_remoto, crontab,tipo_transferencia, log, sh.id_conexion,status from share sh inner join conexionssh cs on sh.id_conexion=cs.id;"
                cursor.execute(sql)
                datos = cursor.fetchall()
                if datos:
                    matriz = []
                    for row in datos:
                        data = {
                        "ID" : row[0],
                        "crontab" : row[3],
                        "tipo_transferencia": row[4],
                        "SOURCE": row[1], 
                        "FINAL" : row[2],
                        "LOG" : row[5],
                        "id_conexion": row[6],
                        "status": row[7]
                        }
                        matriz.append(data) 
                    return(matriz)
                else:
                    return(0)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()