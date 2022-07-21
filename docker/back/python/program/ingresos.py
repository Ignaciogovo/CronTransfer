import sys

def introducirssh():
    data={}
    data["HOST"]=  input("IP Servidor: ") or ("")
    # data["PORT"] = input("puerto: ") or ("")
    data["USER"] = input("usuario: ") or ("")
    data["PASS"] = input("Contraseña: ") or ("")
    if "" in data.values():
        print("Has introducidos datos erroneos")
        sys.exit(1)
    return(data)
def introducirshare():
    data={}
    data["soruce"]=  input("Ruta origen: ") or ("")
    data["final"] = input("rutafinal: ") or ("")
    data["minutes"] = input("minutos: ") or ("")
    data["hours"] = input("horas: ") or ("")
    data["days"] = input("dias: ") or ("")
    data["months"] = input("meses: ") or ("")
    data["weekday"] = input("dias de la semana: ") or ("")
    if "" in data.values():
        print("Has introducidos datos erroneos")
        sys.exit(1)
    return(data)


