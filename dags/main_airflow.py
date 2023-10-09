import requests
import pandas as pd
import os, sys
sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(1, os.path.abspath("../plugins"))
import json
# Se llaman unicamente a las funciones necesarias en los imports de módulos propios
import conexion_db
import config
#from plugins.conexion_db import conectar, crear_tabla, insertar_registro, crear_tabla_staging, upsert_criptomonedas, eliminar_tabla_staging
from test_utils import cast_date
from datetime import timedelta, datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

# Autor: Benjamin Luengo Ackermann

# Repositorio API: https://github.com/fawazahmed0/currency-api#readme

# Argumentos del DAG
default_args={
    'owner': 'Benjamin Luengo Ackermann',
    'start_date': datetime(2023,10,1),
    'retries':1,
    'retry_delay': timedelta(minutes=2),
    # Configuración de argumentos para enviar correos cuando falla el DAG y las tareas 
    'email': config.EMAIL_NOTIFICATION_LIST, 
    'email_on_failure': True,
    'email_on_retry': False
}

# Declaracion del DAG
cripto_dag = DAG(
    dag_id="criptomonedas_ETL",
    default_args=default_args,
    description="ETL de top 10 criptomonedas que corre en forma diaria, tomando su valor en dolares desde una API",
    schedule_interval='@daily', 
    )

def extraccion_datos(ti):

    print("Extraccion de Datos")
    
    # Conexión con API
    response_currencies = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json')
    # Verificamos que la conexión con la API es exitosa
    if(response_currencies.status_code == 200):

        # Casteamos el JSON a un dict
        currencies = response_currencies.json()

        ti.xcom_push(key='extraccion_datos',value=currencies)

    else:
        print("Error de conexión con la API")


def limpieza_de_datos(ti):

    currencies = ti.xcom_pull(key="extraccion_datos", task_ids="extraccion_datos")
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

    # Elegimos 10 cryptos de interés arbitrario
    top_10_crypto = ["btc", "bnb", "eth", "luna", "trx", "cake", "xrp", "matic", "doge", "leo"]

    # Elegimos mediante la funcion loc las 10 criptos de interes (se encuentran en el index del DF)
    df_currencies = df_currencies.loc[top_10_crypto]

    json_currencies = df_currencies.to_json()

    ti.xcom_push(key="df_currencies", value=json_currencies)
    ti.xcom_push(key="top_10_crypto", value=top_10_crypto)
    ti.xcom_push(key="date", value=date)


def carga_datos(ti):

    json_currencies = ti.xcom_pull(key="df_currencies", task_ids="limpieza_de_datos")
    json_currencies = json.loads(json_currencies)
    print(json_currencies)
    df_currencies = pd.DataFrame.from_dict(json_currencies)
    top_10_crypto = ti.xcom_pull(key="top_10_crypto", task_ids="limpieza_de_datos")
    date = ti.xcom_pull(key="date", task_ids="limpieza_de_datos")
    
    # Conectamos a la BD
    conexion, cursor_db = conexion_db.conectar()

    if(conexion):                    
        # Crea la tabla de criptomonedas si no existe
        conexion_db.crear_tabla(cursor_db=cursor_db, conn=conexion)

        # Eliminar tabla staging si existe (no deberia)
        conexion_db.eliminar_tabla_staging(cursor_db=cursor_db, conn=conexion)

        # Crea la tabla de staging
        conexion_db.crear_tabla_staging(cursor_db=cursor_db, conn=conexion)

        for crypto in top_10_crypto:
            # A la hora de insertar en la tabla, se le podria aplicar tecnicas de compresión como RLE al campo fecha para no tener el valor repetido n veces.
            conexion_db.insertar_registro(
                cursor_db=cursor_db,
                conn=conexion,
                nombre=crypto,
                fecha=date,
                # precio_relativo: cuanto vale en la criptomoneda correspondiente una unidad de dolar (e.g: 1 USD = 0.00003845 BTC)
                precio_relativo=float(round(float(df_currencies.loc[crypto, "usd"]), 8)),
                # precio_unitario: cuanto vale en dólares una unidad de la criptomoneda (e.g: 1 BTC = 26010 USD)
                precio_unitario=float(round(1/float(df_currencies.loc[crypto, "usd"]), 8)))
        
        # Realizamos el merge entre la tabla de staging y la persistente
        conexion_db.upsert_criptomonedas(cursor_db=cursor_db, conn=conexion)

"""def get_data_from_api():

    print("Extraccion de Datos")
    
    # Conexión con API
    response_currencies = requests.get('https://cdn.jsdelivr.net/gh/fawazahmed0/currency-api@1/latest/currencies/usd.json')


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

    print("Conexion de BD (TaskGroup para conectar y para insertar)")

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
        upsert_criptomonedas(cursor_db=cursor_db, conn=conexion) """


# Tareas

## 1. Extraccion
"""task_1 = PythonOperator(
    task_id="get_data_from_api",
    python_callable=get_data_from_api,
    dag=cripto_dag
)"""

task_extraccion = PythonOperator(
    task_id="extraccion_datos",
    python_callable=extraccion_datos,
    dag=cripto_dag
)

task_transformacion = PythonOperator(
    task_id="limpieza_de_datos",
    python_callable=limpieza_de_datos,
    dag=cripto_dag
)

task_carga = PythonOperator(
    task_id="carga_datos",
    python_callable=carga_datos,
    dag=cripto_dag
)

# Orden de tareas
#task_1
task_extraccion >> task_transformacion >> task_carga