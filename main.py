import requests
import os
from dotenv import load_dotenv
import time

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_KEY")

def obtener_datos(simbolo, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={simbolo}&apikey={api_key}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    if "Time Series (Daily)" not in datos:
        print(f"Error en {simbolo}: {datos.get('Information', 'Error desconocido')}")
        return None
    serie = datos["Time Series (Daily)"]
    ultima_fecha = list(serie.keys())[0]
    precio_cierre_ultima_fecha = serie[ultima_fecha]["4. close"]
    return {"fecha": ultima_fecha, "cierre": precio_cierre_ultima_fecha}

empresas = ["AAPL", "GOOGL", "MSFT"]

for empresa in empresas:
    resultado = obtener_datos(empresa, api_key)
    if resultado:
        print(f"{empresa} | {resultado['fecha']} | {resultado['cierre']}")
    else:
        print(f"{empresa} | sin datos disponibles")
    time.sleep(15) #para que la API nos permita acceder