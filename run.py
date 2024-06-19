from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='src', static_folder='static')

# Set secret key for session management
app.secret_key = 'your secret key'

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config["MYSQL_PORT"] = 3306
app.config['MYSQL_DB'] = 'shopify'

# Initialize MySQL
conn = MySQL(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        return render_template("index3.html")
    elif request.method == "POST":
        fname = request.form["Fname"]
        lname = request.form["Lname"]
        email = request.form["email"]
        gender = request.form["gender"]
        account_type = request.form["types"]
        phone = request.form["number"]
        password = request.form["password"]
        
        cur = conn.connection.cursor()
        cur.execute("INSERT INTO users(first_name, last_name, email, gender, phone_number, account_type, password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (fname, lname, email, gender, phone, account_type, password))
        conn.connection.commit()
        cur.close()
        
        return render_template("index2.html")
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        cur = conn.connection.cursor()
        cur.execute("SELECT email, password FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        
        if user and password == user[1]:  # Compare plain text password
            session["username"] = user[0]
            return redirect(url_for("shop_now"))
        else:
            return render_template("index4.html", infos="Invalid username or password")

    return render_template("index4.html")

@app.route("/shop_now")
def shop_now():
    return render_template("index2.html")
    # if "username" in session:
    #     return f"Welcome {session['username']} to the shop!"
    # return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# Your other routes and application setup
if __name__ == "__main__":
    app.run(debug=True)
