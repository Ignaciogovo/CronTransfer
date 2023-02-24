
id_borrar=  input("Indica el id de la conexión que desea borrar (Escribir 0 si no desea borrar ninguno): ") or ("0")

try:
    int(id_borrar)
    print("prueba buena")
except: 
    print("Valor incorrecto2")