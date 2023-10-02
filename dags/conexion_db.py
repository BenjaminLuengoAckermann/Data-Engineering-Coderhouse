import psycopg2
import config


def conectar():
    host = config.host
    port = config.port
    dbname = config.dbname
    user = config.user
    password = config.password

    # Conectarse al cluster de Redshift
    try: 
        conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        print(conn)

        # Create un cursor para interactuar con la base de datos
        cursor_db = conn.cursor()

        return conn, cursor_db
    
    except:
        # En caso de no poder conectarse
        return False, False


def crear_tabla(cursor_db, conn):
    create_query = """
    CREATE TABLE IF NOT EXISTS benjaluengoa_coderhouse.criptomonedas (
	nombre varchar(256) NOT NULL,
	fecha date NOT NULL,
	precio_unitario decimal(38, 10) NOT NULL,
	precio_relativo decimal(38, 10) NOT NULL, 
    primary key(nombre, fecha));
    """
    cursor_db.execute(create_query)
    conn.commit()
    

def crear_tabla_staging(cursor_db, conn):
    # Creamos tabla de staging
    staging_table = "CREATE TABLE staging_criptomonedas as (SELECT * FROM criptomonedas WHERE 0 = 1);"
    cursor_db.execute(staging_table)
    conn.commit()


def eliminar_tabla_staging(cursor_db, conn):
    # Creamos tabla de staging
    staging_table = "DROP TABLE IF EXISTS staging_criptomonedas;"
    cursor_db.execute(staging_table)
    conn.commit()


def insertar_registro(cursor_db, conn, nombre, fecha, precio_unitario, precio_relativo):
    # Se insertan los registros en la tabla temporal o de staging
    insert_query = '''
        INSERT INTO staging_criptomonedas (nombre, fecha, precio_unitario, precio_relativo)
        VALUES (%s, %s, %s, %s);
    '''
    cursor_db.execute(insert_query, (str(nombre), fecha, precio_unitario, precio_relativo))
    conn.commit()

    
def upsert_criptomonedas(cursor_db, conn):
    # Se eliminan los duplicados en la tabla de criptomonedas para posteriormente insertar los valores actualizados
    delete_duplicates = """
    DELETE FROM criptomonedas 
    USING staging_criptomonedas
    WHERE criptomonedas.fecha = staging_criptomonedas.fecha AND criptomonedas.nombre = staging_criptomonedas.nombre;
    """
    cursor_db.execute(delete_duplicates)
    conn.commit()

    # Se insertan los valores actualizados
    upsert_query = "INSERT INTO criptomonedas SELECT * FROM staging_criptomonedas;"
    cursor_db.execute(upsert_query)
    conn.commit()

    # Finalmente, se elimina la tabla de staging
    drop_staging = "DROP TABLE staging_criptomonedas;"
    cursor_db.execute(drop_staging)
    conn.commit()