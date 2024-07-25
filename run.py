from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
import os
from werkzeug.utils import secure_filename
import MySQLdb.cursors
from flask import jsonify
from collections import defaultdict



app = Flask(__name__, template_folder='src', static_folder='static')

# Set secret key for session management
app.secret_key = 'your secret key'

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# MySQL configurations
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config["MYSQL_PORT"] = 3306
app.config['MYSQL_DB'] = 'shopify'

# Initialize MySQL
conn = MySQL(app)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
        hashed_password = generate_password_hash(password)


        cur = conn.connection.cursor()
        cur.execute("INSERT INTO userss(first_name, last_name, email, gender, phone_number, account_type, password) VALUES(%s, %s, %s, %s, %s, %s, %s)",
                    (fname, lname, email, gender, phone, account_type, hashed_password))
        conn.connection.commit()
        cur.execute("SELECT id FROM userss WHERE email = %s", (email,))
        user = cur.fetchone()
        session['user_id'] = user[0]
        cur.close()

        cur = conn.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT id, store_name, product_name, price, img_name, stock_amount, created_at FROM product_upload ORDER BY created_at DESC')
        products = cur.fetchall()
        cur.close()
            
        grouped_products = defaultdict(list)
        for product in products:
                grouped_products[product['store_name']].append(product)


        print(f"the user id is {user}")
        
        return render_template("index2.html", grouped_products=grouped_products)
    return render_template("index.html") 


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        try:
            with conn.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
                cur.execute("SELECT id, email, password FROM userss WHERE email = %s", (email,))
                user = cur.fetchone()
                print(f"Fetched user: {user}")  # Debugging: Check fetched user

            if user:
                # Debugging: Print the hashed password from the database
                print(f"Hashed Password from DB: {user['password']}")
                
                # Debugging password check
                password_match = check_password_hash(user['password'], password)
                print(f"Password match: {password_match}")
                
                if password_match:
                    session['user_id'] = user['id']
                    
                    # Fetch products and group them
                    with conn.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
                        cur.execute('SELECT id, store_name, product_name, price, img_name, stock_amount, created_at FROM product_upload ORDER BY created_at DESC')
                        products = cur.fetchall()
                    
                    grouped_products = defaultdict(list)
                    for product in products:
                        grouped_products[product['store_name']].append(product)
                    
                    return render_template("index2.html", grouped_products=grouped_products)
                else:
                    flash('Invalid email or password')
                    print('Invalid email or password')
            else:
                flash('Invalid email or password')
                print('Invalid email or password')
        except Exception as e:
            print(f"An error occurred: {e}")
            flash('An error occurred during login. Please try again.')
        
        return redirect(url_for('login'))

    return render_template("index4.html")



@app.route("/shop_now")
def shop_now():
    try:
        with conn.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
            cur.execute('SELECT id, store_name, product_name, price, img_name, stock_amount, created_at FROM product_upload ORDER BY created_at DESC')
            products = cur.fetchall()
        
        grouped_products = defaultdict(list)
        for product in products:
            grouped_products[product['store_name']].append(product)
        return render_template("index2.html", grouped_products=grouped_products)
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while fetching products. Please try again.')
        return render_template("index2.html")

@app.route("/dashboard")
def dashboard():
    cur = conn.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT id, store_name, product_name, price, img_name, stock_amount, created_at FROM product_upload ORDER BY created_at DESC')
    # cur.execute('SELECT store_name, product_name, price, img_name, stock_amount FROM product_upload')
    products = cur.fetchall()
    cur.close()
    return render_template('index5.html', products=products)
    # return render_template("index5.html")

    
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    store_results = defaultdict(list)
    product_results = []
    grouped_products = {'store_results': store_results, 'product_results': product_results}

    if query:
        try:
            # Get a cursor
            cur = conn.connection.cursor(MySQLdb.cursors.DictCursor)

            # SQL query to search for store_name or product_name
            search_query = """
            SELECT store_name, product_name, price, img_name 
            FROM product_upload 
            WHERE store_name LIKE %s OR product_name LIKE %s
            """

            # Use parameterized query to prevent SQL injection
            cur.execute(search_query, (f'%{query}%', f'%{query}%'))
            products = cur.fetchall()
            cur.close()

            for product in products:
                store_name = product['store_name']
                product_name = product['product_name']

                if query.lower() in store_name.lower():
                    store_results[store_name].append(product)
                if query.lower() in product_name.lower():
                    if store_name in store_results:
                        if product not in store_results[store_name]:
                            store_results[store_name].append(product)
                    else:
                        product_results.append(product)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('error.html', error=str(e))
    
    return render_template('search.html', grouped_products=grouped_products, query=query)



@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        flash('Please log in to add items to your cart.')
        return redirect(url_for('login'))
    
    product = {
        'store_name': request.form.get('store_name'),
        'product_name': request.form.get('product_name'),
        'price': request.form.get('price'),
        'img_name': request.form.get('img_name')
    }
    user_id = session['user_id']

    try:
        with conn.connection.cursor() as cur:
            cur.execute("""
                INSERT INTO cart (store_name, product_name, price, img_name, user_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (product['store_name'], product['product_name'], product['price'], product['img_name'], user_id))
            conn.connection.commit()
        return jsonify({'success': 'Product added to cart!'})
    except Exception as e:
        flash(f'Error adding product to cart: {e}')
        print(f'Error: {e}')

    return redirect(url_for('shop_now'))



@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('Please log in to view your cart.')
        return redirect(url_for('signup'))
    
    user_id = session['user_id']
    try:
        with conn.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM cart WHERE user_id = %s", [user_id])
            cart_items = cur.fetchall()

            total_price = sum(item['price'] for item in cart_items)

        return render_template('cart.html', cart=cart_items, total_price=total_price)
    except Exception as e:
        print(f"An error occurred: {e}")
        flash('An error occurred while fetching your cart. Please try again.')
        return redirect(url_for('home'))


@app.route("/steeze")
def steeze():
    return render_template("index6.html")

@app.route('/delete_product/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    try:
        cur = conn.connection.cursor()
        cur.execute('DELETE FROM product_upload WHERE id = %s', (product_id,))
        conn.connection.commit()
        cur.close()
        return jsonify({'message': 'Product deleted successfully'}), 204 
    except Exception as e:
        return jsonify({'message': str(e)}), 400


@app.route('/remove_from_cart/<int:cart_item_id>', methods=['POST'])
def remove_from_cart(cart_item_id):
    if 'user_id' not in session:
        flash('Please log in to remove items from your cart.')
        return redirect(url_for('login'))

    user_id = session['user_id']
    try:
        with conn.connection.cursor() as cur:
            cur.execute("DELETE FROM cart WHERE id = %s AND user_id = %s", (cart_item_id, user_id))
            conn.connection.commit()
        flash('Product removed from cart!')

        with conn.connection.cursor(MySQLdb.cursors.DictCursor) as cur:
            cur.execute("SELECT * FROM cart WHERE user_id = %s", [user_id])
            cart_items = cur.fetchall()

        total_price = sum(item['price'] for item in cart_items)

        return render_template('cart.html', cart=cart_items, total_price=total_price)

    except Exception as e:
        print(f'Error removing product from cart: {e}')

    return redirect(url_for('cart'))



@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "GET":
        return render_template("index6.html")

    if request.method == "POST":
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect('upload')
        
        file = request.files['file']
        
        # If user does not select a file, browser also submits an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            store_name = request.form["store_name"]
            product_name = request.form["product_name"]
            price = request.form["price"]
            stock_amt = request.form["stock_amt"]
            img_name = filename
            
            cur = conn.connection.cursor()
            cur.execute("INSERT INTO product_upload(store_name, product_name, price, img_name, stock_amount) VALUES(%s, %s, %s, %s, %s)",
                        (store_name, product_name, price, img_name, stock_amt))
            conn.connection.commit()
            cur.close()
            
            flash('File successfully uploaded and data saved')
            return redirect(url_for('upload'))
        else:
            flash('Allowed file types are png, jpg, jpeg, gif, pdf')
            return redirect(url_for('upload'))
        
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))



# Your other routes and application setup
if __name__ == "__main__":
    app.run(debug=True)

    
 

