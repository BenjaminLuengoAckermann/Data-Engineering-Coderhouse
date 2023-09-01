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
    primary key(nombre));
    """
    cursor_db.execute(create_query)
    conn.commit()
    

def insertar_registro(cursor_db, conn, nombre, fecha, precio_unitario, precio_relativo):
    insert_query = """
    INSERT INTO criptomonedas (nombre, fecha, precio_unitario, precio_relativo)
    VALUES (%s, %s, %s, %s);
    """

    cursor_db.execute(insert_query, (nombre, fecha, precio_unitario, precio_relativo))
    conn.commit()
