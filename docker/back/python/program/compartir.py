import sys
import conexionbbdd as bbdd
import funcionesSSH as fssh
def conexionData():
    try:
        id = sys.argv[1]
    except:
        print("El programa no recibe argumentos")
        sys.exit(1)
    try:
        origenfinal = bbdd.consultarOrigenFinal(id)
        idssh= bbdd.consultaridssh(id)
    except:
        print("No es posible conexion con la base de datos o los datos no se han encontrado")
        sys.exit(1)
    try:
        data= bbdd.consultarDatosssh(idssh)
    except:
        print("Problemas al sacar datos a partir del idSSH")    
        sys.exit(1)
    data["SOURCE"] =origenfinal[0]
    data["FINAL"] =origenfinal[1]
    return(data)

data=conexionData()
try:
    fssh.sendfile(data)
except:
    print("No se ha podido enviar el archivo")
    sys.exit(1)