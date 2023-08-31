from datetime import datetime
import requests
from conexion_db import *

# Autor: Benjamin Luengo Ackermann

# Repositorio API: https://github.com/fawazahmed0/currency-api#readme


# Conexión con API
response_currencies = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json')



# Funcion para castear fechas
def cast_date(date):
    if(date):
        date_str = date
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date_str, date_format)
        date = str(date.day) + "/" + str(date.month) + "/" + str(date.year)
        return date
    else: 
        return None


# Verificamos que la conexión con la API es exitosa
if(response_currencies.status_code == 200):

    # Casteamos el JSON a un dict
    currencies = response_currencies.json()

    # Cast de fechas a formato dd/m/yyyy
    date = cast_date(currencies["date"])
    
    # Conectamos a la BD
    conexion, cursor_db = conectar()

    # Elegimos 10 cryptos de interés arbitrario
    top_10_crypto = ["btc", "bnb", "eth", "luna", "trx", "cake", "xrp", "matic", "doge", "leo"]

    if(conexion):            
        # A la hora de insertar en la tabla, se le podria aplicar tecnicas de compresión como RLE al campo fecha para no tener el valor repetido n veces.
        # Teniendo en cuenta que en una BD Relacional la tabla tendria por columnas 
            # nombre (unique) (varchar(256))
            # fecha (date)
            # precio_unitario (decimal(38, 10)) --> cuanto vale en dólares una unidad de la criptomoneda (e.g: 1 BTC = 26010 USD)
            # precio_relativo (numeric(38, 10)) --> cuanto vale en la criptomoneda correspondiente una unidad de dolar (e.g: 1 USD = 0.00003845 BTC)  
        # En base a estas columnas y recordando que una BD Columnar consiste en pivotear la tabla relacional 
        # se obtendrán como filas el nombre, fecha, precio_unitario y precio_relativo
        
        # Crea la tabla si no existe
        crear_tabla(cursor_db=cursor_db, conn=conexion)

        for crypto in top_10_crypto:
            insertar_registro(
                cursor_db=cursor_db,
                conn=conexion,
                nombre=crypto,
                fecha=currencies["date"],
                precio_relativo=float(round(float(currencies["usd"][crypto]), 8)),
                precio_unitario=float(round(1/float(currencies["usd"][crypto]), 8)))


# En caso de no poder conectarnos con la API
else:
    print("Error de conexión con la API")