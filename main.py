from datetime import datetime
import requests

""" Autor: Benjamin Luengo Ackermann

    Para este proyecto se eligió una API de acceso público y gratuito (sin auth) que devuelve 
    los datos de la cotización al final del dia de mas de 150 de las principales criptomonedas del mercado.
    De esta manera obtenemos un JSON con el nombre de la criptomoneda (e.g: BTC) y su cotización equivalente a un dolar, es decir
    cuanto vale 1 USD en esa criptomoneda. 
    Adicionalmente, se calcula el valor de una unidad de la criptomoneda (e.g: 1 BTC) y su equivalencia en dólares.

    La intención es almacenar día a día los valores de la cotización y así lograr una línea histórica para cada criptomoneda.

    Se puede pensar este script como uno que se corre diariamente dentro de una organización a fin de obtener las cotizaciones y almacenarlas
    con el objetivo de lograr consultas que agreguen valor a la compañia en una linea  temporal histórica desde el primer día de puesta en marcha
    del script hasta la actualidad."""

# Repositorio API: https://github.com/fawazahmed0/currency-api#readme


# Conexión con API
response_currencies = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json')

# Funcion para definir la cantidad de cryptos a mostrar
def input_corte():
    input_valido = False
    corte = 0
    while not input_valido: 
        try: 
            corte = int(input("Ingrese la cantidad de cryptos que quiere mostrar (si desea mostrar todas ingrese 0): "))
            if(type(corte) != int or corte < 0):
                print("Ingrese un valor valido.")
            else:
                input_valido = not input_valido
                
        except: 
           print("Ingrese un valor valido.")
    
    return corte

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

    # El valor de corte es únicamente para el print, el diccionario contiene todas las criptomonedas independientemente del corte ingresado
    corte = input_corte()

    print("\nListado Crypto - {}".format(date))
    cont = 0
    for crypto in currencies["usd"]:
        cont += 1
        print("\t" + crypto.upper() + "\n" 
            + "\t\t{}".format(str(currencies["usd"][crypto]))
            + " " + crypto.upper() 
            + " = 1 USD"
            + "\n\t\t"
            + "1 " + crypto.upper()
            # Cálculo del valor de una unidad de la criptmoneda y su equivalencia en dolares (e.g: 1 BTC = 26010 USD)
            + " = " + str(1/currencies["usd"][crypto]) + " USD")
        if(corte > 0 and cont == corte):
            break
    
    # A la hora de insertar en la tabla, se le podria aplicar tecnicas de compresión como RLE al campo fecha para no tener el valor repetido n veces.
    # Teniendo en cuenta que en una BD Relacional la tabla tendria por columnas 
        # nombre (unique)
        # fecha
        # precio_unitario --> cuanto vale en dólares una unidad de la criptomoneda (e.g: 1 BTC = 26010 USD)
        # precio_relativo --> cuanto vale en la criptomoneda correspondiente una unidad de dolar (e.g: 1 USD = 0.00003845 BTC)  
    # En base a estas columnas y recordando que una BD Columnar consiste en pivotear la tabla relacional 
    # se obtendrán como filas el nombre, fecha, precio_unitario y precio_relativo

# En caso de no poder conectarnos con la API
else:
    print("Error de conexión con la API")