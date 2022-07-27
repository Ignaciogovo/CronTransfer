import conexionbbdd
data={}
data["HOST"]=  "192.168.1.90"
data["PORT"] = "22"
data["USER"] = "pi"
data["PASS"] = "prueba"
conexionbbdd.ingresarSSH(data)