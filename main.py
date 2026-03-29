import requests
import os
from dotenv import load_dotenv
import time
import sqlite3
from datetime import date

load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_KEY")

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

def guardar_datos(empresa, historico):
    for dia in historico:
        cursor.execute("""
            INSERT INTO precios (empresa, fecha, cierre)
            VALUES (?, ?, ?)
        """, (empresa, dia['fecha'], dia['cierre']))

def leer_datos(simbolo):
    cursor.execute("""
        SELECT * FROM precios WHERE empresa = ?
    """, (simbolo,))
    resultados = cursor.fetchall()
    return resultados

def tengo_datos_hoy(simbolo):
    hoy = date.today()
    cursor.execute("""
        SELECT * FROM precios WHERE empresa = ? AND fecha = ?
    """, (simbolo, hoy))
    resultado = cursor.fetchone()
    return resultado is not None

empresas = ["AAPL", "GOOGL", "MSFT"]

for empresa in empresas:
    if tengo_datos_hoy(empresa):
        print(f"{empresa} | ya tenemos datos de hoy, leyendo de la BBDD")
        resultado = leer_datos(empresa)
        for fila in resultado:
            print(fila)
    else:
        resultado = obtener_datos(empresa, api_key)
        if resultado:
            guardar_datos(empresa, resultado)
        else:
            print(f"{empresa} | sin datos disponibles")
        time.sleep(15)

conexion.commit()
conexion.close()