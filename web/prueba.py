#Beatiful soup
#Instalamos librerias (Desde el terminal: pip install bs4 ) instalamos tambien (pip install requests)
#Instalamos pandas: pip install pandas
# Descargarmos desde el terminal pip install lxml (Con esto podemos leer paginas html) //No se usa porqu esta pandas
from itertools import count
from operator import eq
from bs4 import BeautifulSoup
import requests
import pandas as pd

#Ponemos el link de la pagina: #Vamos a obtener todos los equipos de la clasificación as
url = 'https://crontab-generator.org'
page=requests.get(url) #Obtenemos la pagina
soup = BeautifulSoup(page.content, 'html.parser') #Para obtenerlos de una forma html
# print(soup)
f = open("codigo.txt", "a")
f.write(str(soup))
f.close()