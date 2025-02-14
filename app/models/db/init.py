import connection as db
import psycopg2

def init(connection, cursor):
    try:
        if cursor is not None:
            with open("../dbScript/create.sql", "r") as create_file:
                create_sql = create_file.read()
                cursor.execute(create_sql)       

            with open("../dbScript/insert.sql", "r") as insert_file:
                insert_sql = insert_file.read()
                cursor.execute(insert_sql)       

            connection.commit() 
            print("Base de données initialisée avec succès")
            return True
    except Exception as e:
        print("Erreur lors de l'initialisation de la base de données :", e)
        connection.rollback()
        db.close_connection(connection, cursor)
        return False
    
### Main ###

conn = db.connection()
cur = conn.cursor()    
try:
    is_init = init(conn, cur)
except psycopg2.OperationalError as e:
    print(f"Echec de la connection {e}")
    db.close_connection(conn, cur)
        