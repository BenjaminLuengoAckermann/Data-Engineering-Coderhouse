import psycopg2

def conectar():
    host = "data-engineer-cluster.cyhh5bfevlmn.us-east-1.redshift.amazonaws.com"
    port = "5439"
    dbname = "data-engineer-database"
    user = "benjaluengoa_coderhouse"
    password = ""

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
        return False, False

    
def insertar_registro(cursor_db, conn, nombre, fecha, precio_unitario, precio_relativo):
    insert_query = """
    INSERT INTO criptomonedas (nombre, fecha, precio_unitario, precio_relativo)
    VALUES (%s, %s, %s, %s);
    """

    cursor_db.execute(insert_query, (nombre, fecha, precio_unitario, precio_relativo))
    conn.commit()
