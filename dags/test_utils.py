from datetime import datetime


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


def print_listado(currencies, date, corte):
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


# Funcion para castear fechas
def cast_date(date):
    if(date):
        date_str = date
        date_format = "%Y-%m-%d"
        date = datetime.strptime(date_str, date_format)
        date = str(date.year) + "/" + str(date.month) + "/" + str(date.day)
        return date
    else: 
        return None