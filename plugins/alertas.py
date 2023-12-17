from conexion_db import avg_criptos

def outliers(cursor_db, conn, pd):

    averages = avg_criptos(cursor_db=cursor_db, conn=conn, pd=pd)
    print(averages)
    return averages


def get_tresholds_for_top_10_crypto(crypto):
    # Los valores de los tresholds (deben ser > 0) se pueden cambiar desde aquí permitiendo personalizar el envio de alertas
    dict = {
        "btc": 2000,
        "bnb": 3,
        "eth": 2000,
        "luna": 3,
        "trx": 2,
        "cake": 2,
        "xrp": 2,
        "matic": 2,
        "doge": 2,
        "leo": 2
    }
    return dict[crypto]


def check_if_outlier(valor_df, promedio, crypto):
    # Evalua si los valores del dia estan fuera de los rangos permitidos en cada cripto
    print(valor_df)
    print(promedio)
    variacion = get_tresholds_for_top_10_crypto(crypto=crypto)

    # Si alguno de los valores es negativo, estamos hablando de un outlier. Primero se chequea el valor diario
    if(valor_df < 0):
        return {"boolean": True, "message": "El valor diario de la criptomoneda es menor a 0."}
    else:
        # Cheque promedio historico
        if(promedio < 0):
            return {"boolean": True, "message": "El valor del promedio historico de la criptomoneda es menor a 0"}
        # Chequeo treshold elegido
        elif (variacion < 0):
            return {"boolean": True, "message": "El valor elegido como treshold es menor a 0."}
        
    # Si los valores de las criptos exceden el promedio historico en un rango customizable, se considera outlier
    # El valor diario esta por encima del promedio historico mas la variacion
    if(promedio + variacion <= valor_df):
        return {"boolean": True, 
                "message": """El valor diario de la criptomoneda ({}) se encuentra POR ARRIBA del promedio historico ({})
                  SUMADO a la variacion elegida ({}). Es decir, la criptomoneda supera el valor {}"""
                  .format(valor_df, promedio, variacion, (promedio + variacion))}
    # El valor diario esta por debajo del promedio historico menos la variacion
    elif (promedio - variacion >= valor_df):
        return {"boolean": True, 
                "message": """El valor diario de la criptomoneda ({}) se encuentra POR DEBAJO del promedio historico ({})
                  RESTADO a la variacion elegida ({}). Es decir, la criptomoneda no supera el valor {}"""
                  .format(valor_df, promedio, variacion, (promedio - variacion))}
    
    # Caso que no supere el rango y sea un valor >= 0, se considera un valor "normal"
    return {"boolean": False}
