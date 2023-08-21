from datetime import datetime
import requests

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

    # Cast de fechas
    date = cast_date(currencies["date"])

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
            + " = " + str(1/currencies["usd"][crypto]) + " USD")
        if(corte > 0 and cont == corte):
            break
# En caso de no poder conectarnos con la API
else:
    print("Error de conexión con la API")