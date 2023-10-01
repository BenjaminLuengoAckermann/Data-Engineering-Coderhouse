import requests
import pandas as pd
# Se llaman unicamente a las funciones necesarias en los imports de módulos propios
from conexion_db import conectar, crear_tabla, insertar_registro, crear_tabla_staging, upsert_criptomonedas, eliminar_tabla_staging
from test_utils import cast_date
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Autor: Benjamin Luengo Ackermann

# Repositorio API: https://github.com/fawazahmed0/currency-api#readme

default_args={
    'owner': 'Benjamin Luengo Ackermann',
    'start_date': datetime(2023,10,1),
    'retries':1,
    'retry_delay': timedelta(minutes=2)
}

critpo_dag = DAG(
    dag_id="criptomonedas_ETL",
    default_args=default_args,
    description="ETL de top 10 criptomonedas que corre en forma diaria",
    schedule_interval='@daily'
    )

print("INICIANDO")


def get_data_from_api():
    # No se usa el parametro de fecha en la funcion debido a que la API siempre trae los registros del dia anterior, siendo redundante usar la fecha como parametro
    print("Extraccion de Datos")
    # Conexión con API
    response_currencies = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json')


#def data_cleaning(response_currencies):
    print("Limpieza de Datos")
    # Verificamos que la conexión con la API es exitosa
    if(response_currencies.status_code == 200):

        # Casteamos el JSON a un dict
        currencies = response_currencies.json()

        # Cast de fechas a formato dd/m/yyyy
        date = cast_date(currencies["date"])
        
        # Parseamos el diccionario a un DF para poder sanear los datos
        df_currencies = pd.DataFrame.from_dict(currencies)

        # Borramos los espacios en blanco innecesarios al comienzo o final del indice (nombre de la criptomoneda)
        df_currencies.index = df_currencies.index.str.strip()
        
        # Convertimos a minusculas el nombre de la criptomoneda
        df_currencies.index = df_currencies.index.str.lower()

        # Casteamos la columna 'date' al tipo de datos datetime para que corresponda con la BD
        df_currencies["date"] = pd.to_datetime(df_currencies["date"])
        df_currencies["date"] = df_currencies["date"].dt.date


    # En caso de no poder conectarnos con la API
    else:
        print("Error de conexión con la API")


#def conexion_db(df_currencies):
    print("Conexion de BD")

    # Conectamos a la BD
    conexion, cursor_db = conectar()

    # Elegimos 10 cryptos de interés arbitrario
    top_10_crypto = ["btc", "bnb", "eth", "luna", "trx", "cake", "xrp", "matic", "doge", "leo"]

    # Elegimos mediante la funcion loc las 10 criptos de interes (se encuentran en el index del DF)
    df_currencies = df_currencies.loc[top_10_crypto]

    if(conexion):                    
        # Crea la tabla de criptomonedas si no existe
        crear_tabla(cursor_db=cursor_db, conn=conexion)

        # Eliminar tabla staging si existe (no deberia)
        eliminar_tabla_staging(cursor_db=cursor_db, conn=conexion)

        # Crea la tabla de staging
        crear_tabla_staging(cursor_db=cursor_db, conn=conexion)

        for crypto in top_10_crypto:
            # A la hora de insertar en la tabla, se le podria aplicar tecnicas de compresión como RLE al campo fecha para no tener el valor repetido n veces.
            insertar_registro(
                cursor_db=cursor_db,
                conn=conexion,
                nombre=crypto,
                fecha=date,
                # precio_relativo: cuanto vale en la criptomoneda correspondiente una unidad de dolar (e.g: 1 USD = 0.00003845 BTC)
                precio_relativo=float(round(float(df_currencies.loc[crypto, "usd"]), 8)),
                # precio_unitario: cuanto vale en dólares una unidad de la criptomoneda (e.g: 1 BTC = 26010 USD)
                precio_unitario=float(round(1/float(df_currencies.loc[crypto, "usd"]), 8)))
        
        # Realizamos el merge entre la tabla de staging y la persistente
        upsert_criptomonedas(cursor_db=cursor_db, conn=conexion)


# Tareas

## 1. Extraccion
task_1 = PythonOperator(
    task_id="get_data_from_api",
    python_callable=get_data_from_api,
    dag=critpo_dag
)


## 1. Transformacion
"""task_2 = PythonOperator(
    task_id="data_cleaning",
    python_callable=data_cleaning,
    op_args=["{{ response_currencies }}"],
    dag=critpo_dag
)"""


## 1. Carga
"""task_3 = PythonOperator(
    task_id="conexion_db",
    python_callable=conexion_db,
    op_args=["{{ df_currencies }}"],
    dag=critpo_dag
)"""

# Orden de tareas
task_1