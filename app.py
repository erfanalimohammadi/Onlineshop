import mysql.connector
from flask import Flask, request, render_template, redirect

def check_and_create_database(host, user, password, database):
    try:
        db_connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = db_connection.cursor()
        cursor.execute("SELECT 1 FROM customers LIMIT 1") 
        row = cursor.fetchone()
        if row:
            print("Table 'customers' already exists!")
        else:
            create_table(cursor)  
        db_connection.commit()
        print("Successfully connected to database:", database)
    except mysql.connector.Error as err:
        if err.errno == 1049:
            print("Database", database, "does not exist. Creating database...")
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password
            )
            cursor = db_connection.cursor()
            cursor.execute("CREATE DATABASE " + database)
            print("Database", database, "created successfully.")
            print("Reconnecting to newly created database:", database)
            cursor.close()
            db_connection.close()

            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = db_connection.cursor()

            create_table(cursor) 
            db_connection.commit()
            print("Successfully connected to newly created database:", database)
        else:
            print("Error:", err)
    finally:
        if 'db_connection' in locals() and db_connection.is_connected():
            cursor.close()
            db_connection.close()

def create_table(cursor):
    try:
        cursor.execute("CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, Name VARCHAR(255), Username VARCHAR(255), Phone_number VARCHAR(255), Email VARCHAR(255), Password VARCHAR(255))")
        print("Table 'customers' has been successfully created!")
    except mysql.connector.Error as error:
        print("Error creating table:", error)

host = "localhost"
user = "onlineshop"
password = "123456789"
database = "online_shop"

check_and_create_database(host, user, password, database)

app = Flask(__name__)

@app.route('/loginmain', methods=['GET', 'POST'])
def loginmain():
    user = None  # Initialize user outside try block
    if request.method == 'POST':
        Username = request.form['Username']
        Password = request.form['Password']

        try:
            db_connection = mysql.connector.connect(
                host="localhost",
                user="onlineshop",
                password="123456789",
                database="online_shop"
            )
            cursor = db_connection.cursor()

            cursor.execute("SELECT * FROM customers WHERE Username = %s AND Password = %s", (Username, Password))
            user = cursor.fetchone()

            if user:
                return redirect('/profile')
            else:
                return "Invalid Username or Password"

        except mysql.connector.Error as err:
            return "Database error: {}".format(err)

        finally:
            if 'db_connection' in locals() and db_connection.is_connected():
                cursor.close()
                db_connection.close()
    return render_template('loginmain.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        Name = request.form['Name']
        Username = request.form['Username']
        Phone_number = request.form['Phone-number']
        Email = request.form['Email']
        Password = request.form['Password']

        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = db_connection.cursor()
            cursor.execute("INSERT INTO customers (Name, Username, Phone_number, Email, Password) VALUES (%s, %s, %s, %s, %s)", (Name, Username, Phone_number, Email, Password))
            db_connection.commit()
            return redirect('/loginmain')
        except mysql.connector.Error as err:
            return "Error registering user: {}".format(err)
        finally:
            if 'db_connection' in locals() and db_connection.is_connected():
                cursor.close()
                db_connection.close()

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if request.method == 'POST':
        Email = request.form['Email']
        
        def search_for_user(Email, host, user, password, database):
            try:
                db_connection = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password,
                    database=database
                )
                cursor = db_connection.cursor()

                cursor.execute("SELECT Email FROM customers WHERE Email = %s", (Email,))
                result = cursor.fetchone()

                cursor.close()
                db_connection.close()

                return result
            except mysql.connector.Error as err:
                print("Database error:", err)
                return None
        
        client = search_for_user(Email, host, user, password, database)
        
        if client:
            return redirect ('/forgotpassword2')
        else:
            return "Email not found. Please try again."
    return render_template('forgotpassword.html')

@app.route('/forgotpassword2', methods=['GET', 'POST'])
def new_password():
    if request.method == 'POST':
        email = request.form['Email']
        password = request.form['Password']
        confirm_password = request.form['ConfirmPassword']
        
        if password != confirm_password:
            return "Passwords do not match. Please try again."
        
        try:
            db_connection = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            cursor = db_connection.cursor()

            # Update the password in the database
            cursor.execute("UPDATE customers SET Password = %s WHERE Email = %s", (password, email))
            db_connection.commit()

            cursor.close()
            db_connection.close()

            return "Password reset successfully!"
        except mysql.connector.Error as err:
            print("Database error:", err)
            return "Failed to reset password. Please try again."
    else:
        # نمایش فرم جدید
        return render_template('forgotpassword2.html')


if __name__ == '__main__':
    app.run(debug=True)