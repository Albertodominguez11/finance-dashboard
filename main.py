import requests
import os
from dotenv import load_dotenv
import time
import sqlite3

conexion = sqlite3.connect("finanzas.db") #conectate a la BBDD que esta en el archivo finanzas.db (si no existe lo crea)
cursor = conexion.cursor() #intermediario entre la BBDD y python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS precios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        empresa TEXT,
        fecha TEXT,
        cierre REAL
    )
""")

load_dotenv()

api_key = os.getenv("ALPHA_VANTAGE_KEY")

def obtener_datos(simbolo, api_key):
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={simbolo}&apikey={api_key}"
    respuesta = requests.get(url)
    datos = respuesta.json()
    historico = []

    if "Time Series (Daily)" not in datos:
        print(f"Error en {simbolo}: {datos.get('Information', 'Error desconocido')}")
        return None
    serie = datos["Time Series (Daily)"]

    for fecha, precios in serie.items():
        historico.append({"fecha": fecha, "cierre": precios["4. close"]}) #en la BBDD cada fila sera un diccionario
        
    return historico

empresas = ["AAPL", "GOOGL", "MSFT"]

for empresa in empresas:
    resultado = obtener_datos(empresa, api_key)

    if resultado:
        for dia in resultado: 
            print(f"{empresa} | {dia['fecha']} | {dia['cierre']}")
            cursor.execute("""
                INSERT INTO precios (empresa, fecha, cierre)
                VALUES (?, ?, ?)
            """, (empresa, dia['fecha'], dia['cierre']))
    else:
        print(f"{empresa} | sin datos disponibles")
    time.sleep(15) #para que la API nos permita acceder

conexion.commit()
conexion.close()