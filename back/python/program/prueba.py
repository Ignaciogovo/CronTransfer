import prueba_poo
import f_consultas as f_c
import sys



try:
    menu= sys.argv[1]
except:
    menu = "a"
if menu == "c":
    f_c.c_ssh()

elif menu =="s":
    f_c.c_servicio()

elif menu == "a":
    f_c.c_ssh()
    print("")
    print("---------------")
    print("")
    f_c.c_servicio()

else:
    print("No se reconoce los parametros")
 
