import mysql.connector

def check_database_exists(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = db_connection.cursor()

        cursor.execute("SHOW DATABASES")
        databases = cursor.fetchall()

        for db in databases:
            if db[0] == database:
                return True

        return False

    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)
        return False

def create_database(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        cursor = db_connection.cursor()

        cursor.execute("CREATE DATABASE IF NOT EXISTS " + database)
        print("Database with the name", database, "has been successfully created!")

    except mysql.connector.Error as error:
        print("Error creating database:", error)

    finally:
        if db_connection.is_connected():
            cursor.close()
            db_connection.close()
            print("Connection to MySQL closed.")

def connect_to_database(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connection to the database", database, "has been successfully established!")
        return db_connection

    except mysql.connector.Error as error:
        print("Error connecting to MySQL:", error)
        return None

def create_table(cursor):
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                First_name VARCHAR(255),
                Last_name VARCHAR(255),
                User_name VARCHAR(255),
                Password VARCHAR(255),
                Email VARCHAR(255),
                Phone_number VARCHAR(20)
            )
        """)
        print("Table has been successfully created!")

    except mysql.connector.Error as error:
        print("Error creating table:", error)

# Database information
host = "localhost"
user = "onlineshop"
password = "123456789"
database = "online_shop"

if check_database_exists(host, user, password, database):
    db_connection = connect_to_database(host, user, password, database)
else:
    create_database(host, user, password, database)
    db_connection = connect_to_database(host, user, password, database)

# If connected to the database, create the table
if db_connection:
    cursor = db_connection.cursor()
    create_table(cursor)
