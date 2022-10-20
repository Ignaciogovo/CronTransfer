import f_consultas as f_c
import sys



try:
    menu= sys.argv[1]
except:
    print("Es necesario incluir un argumento")
    sys.exit(1)
if menu == "1":
    f_c.c_ssh()

elif menu =="2":
    f_c.c_servicio()

elif menu == "3":
    f_c.c_ssh()
    print("")
    print("---------------")
    print("")
    f_c.c_servicio()

else:
    print("No se reconoce los argumentos")






