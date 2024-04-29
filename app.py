from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

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
                Name VARCHAR(255),
                Username VARCHAR(255),
                Phone_number VARCHAR(20),
                Email VARCHAR(255),
                Password VARCHAR(255)
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

db_connection = connect_to_database(host, user, password, database)
if db_connection:
    cursor = db_connection.cursor()
    create_table(cursor)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        phone_number = request.form['phone_number']
        email = request.form['email']
        password = request.form['password']

        try:
            cursor.execute("INSERT INTO customers (Name, Username, Phone_number, Email, Password) VALUES (%s, %s, %s, %s, %s)",
                           (name, username, phone_number, email, password))
            db_connection.commit()
            return "Registration successful!"
        except mysql.connector.Error as error:
            return "Error occurred while registering: {}".format(error)

    return render_template('/')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/loginmain', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # اینجا باید بررسی اطلاعات کاربر و اعتبارسنجی انجام شود
        # به عنوان مثال:
        if username == 'admin' and password == 'password':
            return "Login successful!"
        else:
            return "Invalid username or password."

    return render_template('loginmain.html')


@app.route('/forgotpassword', methods=['POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        
        # اینجا باید عملیات بازیابی رمز عبور انجام شود
        # به عنوان مثال، می‌توانید ایمیل را بررسی کنید و یک لینک بازیابی رمز عبور ارسال کنید

        # در انتها پیامی به کاربر نمایش داده می‌شود
        return "An email has been sent to {} for password reset.".format(email)

    # اگر درخواست POST نبود، به صفحه forgotpassword برمی‌گردیم
    return render_template('forgotpassword.html')


@app.route('/forgotpassword2', methods=['POST'])
def reset_password():
    if request.method == 'POST':
        # دریافت ایمیل و رمز عبور جدید از فرم
        email = request.form['email']
        new_password = request.form['password']

        # انجام فرآیند تغییر رمز عبور، مثلا به کمک کتابخانه‌هایی مانند Flask-Security
        # اینجا یک مثال ساده از تغییر رمز عبور را ارائه می‌دهم:
        # یافتن کاربر با استفاده از ایمیل و اعمال تغییرات
        user = User.query.filter_by(email=email).first()
        if user:
            # تغییر رمز عبور کاربر
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return "Password has been successfully updated!"

    return "Failed to update password. Please try again."

