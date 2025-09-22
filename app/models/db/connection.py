import psycopg2

HOST = "172.18.0.2"
USER = "user"
PASSWORD = "secret"
DATABASE = "library-db"


def connection():
    if HOST != "" and USER != "" and PASSWORD != "" and DATABASE != "":
        connection = psycopg2.connect(
            "host=%s dbname=%s user=%s password=%s" % (HOST, DATABASE, USER, PASSWORD)
        )
        print("Connecté à la base de données " + DATABASE + " du serveur " + HOST)
        return connection
    print(
        "Les paramètres pour établir la connection avec la base de données sont vide "
    )
    raise psycopg2.OperationalError


def close_connection(connection, cursor):
    if connection:
        cursor.close()
        connection.close()
        print("Déconnecté de la base de données")
