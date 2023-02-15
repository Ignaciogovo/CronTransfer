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
        self.conn = pymysql.connect(
            host=self.host, 
            user=self.user, 
            password=self.password, 
            database=self.database, 
            charset=self.charset
        )
        print("Conexión establecida")

    def disconnect(self):
        if self.conn is not None:
            self.conn.close()
    
    # Realizar ingresos:
    def insert_ssh(self,data):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "INSERT INTO conexionssh(IP,port,user,tipo,pass,clave) VALUES ({},{},{},{},{},{})".format(data["HOST"],data["PORT"],data["USER"],data["TIPO"],data["PASS"],data["CLAVE"])
                cursor.execute(sql)
                self.conn.commit()
                print("Datos insertados correctamente.")
        except Exception as e:
            print("Error al insertar datos: ", e)
            self.conn.rollback()
        finally:
            self.disconnect()    

    def insert_share(self, data):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                # Comprobar si la clave foránea existe
                cursor.execute("SELECT * FROM conexionssh WHERE id=%s",data["id_conexion"])
                result = cursor.fetchone()
                if result is None:
                    print("La clave foránea no existe.")
                    return

                # Insertar datos
                sql = "INSERT INTO share(origen,final,id_conexion,crontab,log,sobrescribir) VALUES ({},{},{},{},{},{})".format(data["SOURCE"],data["FINAL"],data["id_conexion"],data["crontab"],data["log"],data["SOBRESCRIBIR"])
                cursor.execute(sql)
                self.conn.commit()
                print("Datos insertados correctamente.")

        except Exception as e:
            print("Error al insertar datos: ", e)
        finally:
            self.disconnect()

    # Realizar updates:
    def update_status(self,id,status):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "update share set `status`={} where id={};".format(id,status)
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print("Error al actualizar datos: ", e)
        finally:
            self.disconnect()
    
    # Realizar deletes:
    def delete_ssh(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "delete from conexionssh where id={};".format(id)
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print("Error al borrar datos: ", e)
        finally:
            self.disconnect()


    def delete_share(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "delete from share where id={};".format(id)
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print("Error al borrar datos: ", e)
        finally:
            self.disconnect()

    def delete_share_conexion(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "delete from share where id={};".format(id)
                cursor.execute(sql)
                self.conn.commit()
        except Exception as e:
            print("Error al borrar datos: ", e)
        finally:
            self.disconnect()



# Consultas a la base de datos

#########################################################################
# Consultas en tabla conexionssh:
########################################################################
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
                sql = "select id, IP,port, user, tipo, fecha from conexionssh;"
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
    def select_share_id_conexion(self,id):
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
    
    def select_share_origen_final(self,id):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select origen,final,sobrescribir from share where id=%s;"
                cursor.execute(sql,id)
                resultado = cursor.fetchone()
                return(resultado)
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
# Consultas en varias tablas:
#########################################################################

    def select_todo(self):
        try:
            self.connect()
            with self.conn.cursor() as cursor:
                sql = "select  sh.id, origen, final, crontab, log, sh.id_conexion,status from share sh inner join conexionssh cs on sh.id_conexion=cs.id;"
                cursor.execute(sql)
                datos = cursor.fetchall()
                if datos:
                    matriz = []
                    for row in datos:
                        data = {
                        "ID" : row[0],
                        "SOURCE": row[1], 
                        "FINAL" : row[2],
                        "crontab" : row[3],
                        "LOG" : row[4],
                        "id_conexion": row[5],
                        "status": row[6]
                        }
                        matriz.append(data) 
                    return(matriz)
                else:
                    return(0)
        except Exception as e:
            print("Error al consultar datos: ", e)
        finally:
            self.disconnect()