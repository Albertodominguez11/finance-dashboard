import requests
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_KEY")

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=AAPL&apikey={api_key}"

respuesta = requests.get(url)

datos = respuesta.json()

#print(datos.keys()) #vemos que es diccionario
serie = datos["Time Series (Daily)"] #coge la primera fecha
ultima_fecha = list(serie.keys())[0] #la convierte en lista para poder indexar, y cogemos la primera
print(f"Fecha: {ultima_fecha}")
print(f"Apertura: {serie[ultima_fecha]['1. open']}")
print(f"Cierre: {serie[ultima_fecha]['4. close']}")
