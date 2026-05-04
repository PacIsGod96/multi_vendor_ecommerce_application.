from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from sqlalchemy import create_engine, text, bindparam
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

app.secret_key = os.urandom(24)

conn_str = "mysql://root:cset155@localhost/multi_vendor_ecommerce"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/template')
def view_template():
    return render_template("template.html")

@app.route('/', methods= ['GET']) #Handles getting the login/register page
def login_register():
    return render_template("index.html")

@app.route('/register', methods = ['POST']) #Handles sending info from the sign up 
def register_post():
    username = request.form.get('register_username')
    password = request.form.get('register_password')
    first_name = request.form.get('register_first_name')
    last_name = request.form.get('register_last_name')
    email = request.form.get('register_email')
    role = request.form.get('register_role')

    sql = text("""
        INSERT INTO accounts
        (first_name, last_name, username, password, email_address, role)
        VALUES
        (:FirstName, :LastName, :Username, :Password, :EmailAddress, :Role)
    """)

    conn.execute(sql, {
        'FirstName': first_name,
        'LastName': last_name,
        'Username': username,
        'Password': generate_password_hash(password),
        'EmailAddress': email,
        'Role': role
    })

    conn.commit()

    return render_template('index.html')

@app.route('/login', methods = ['POST']) #handles sending the info from login to compare and the let the user login
def login():
    username = request.form.get('login_username')
    password = request.form.get('login_password')

    sql = text("""
        SELECT username, password, role
        FROM accounts
        WHERE username = :Username
    """)
    result = conn.execute(sql, {'Username': username}).mappings().fetchone()
    print("Entered username: ", username)
    print("DB result: ", result)

    if result:
        stored_password = result['password']
        role = result['role']

        if check_password_hash(stored_password, password):
            session['username'] = result['username']
            session['role'] = role

            return redirect(url_for('products_page'))
        else: 
            return "Incorrect password", 401
    else:
        return "Username not found", 404 
        
    return render_template('index.html')

@app.route('/logout', methods = ['GET']) #Handles loging out
def logout():
    session.clear()
    return redirect(url_for('login_register'))

@app.route('/products', methods = ['GET']) #Handles getting all of the products and their info
def products_page():
    vendors = conn.execute(
        text("SELECT account_id, username FROM accounts WHERE role = 'vendor'")).fetchall()
    return render_template('products.html', vendors=vendors)

@app.route('/add_product', methods=['POST'])
def add_product():

    name = request.form.get('name')
    price = request.form.get('price')

    sizes = request.form.getlist('sizes')
    colors = request.form.getlist('colors')

    vendor_id = session.get('user_id')

    sql = text("""
        INSERT INTO product (name)
        VALUES (:name)
    """)

    result = conn.execute(sql, {'name': name})
    conn.commit()

    product_id = result.lastrowid

    sql2 = text("""
        INSERT INTO vendor_product (vendor_id, product_id, price, available_inventory)
        VALUES (:vendor_id, :product_id, :price, 100)
    """)

    conn.execute(sql2, {
        'vendor_id': vendor_id,
        'product_id': product_id,
        'price': price
    })

    conn.commit()

    for size in sizes:
        conn.execute(text("""
            INSERT INTO product_sizes (product_id, size)
            VALUES (:pid, :size)
        """), {'pid': product_id, 'size': size})

    for color in colors:
        if color.strip(): 
            conn.execute(text("""
                INSERT INTO product_colors (product_id, color)
                VALUES (:pid, :color)
            """), {'pid': product_id, 'color': color})
    conn.commit()
    return redirect(url_for('products_page'))

@app.route('/add_to_cart', methods = ['POST']) #Handles adding the product to the cart
def add_to_cart():
    return render_template('products.html')

@app.route('/send_review_complaint', methods = ['POST']) #Handles sending a review on the product
def send_review_complaint():
    return render_template('products.html')

@app.route('/send_chat', methods = ['POST']) #Hadles sending a chat to the vendor
def send_chat():
    data = request.get_json()

    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
    text_msg = data['text']

    sql = text("""
        INSERT INTO chat (sender_id, receiver_id, text)
        VALUES (:sender_id, :receiver_id, :text)
    """)

    conn.execute(sql, {
        "sender_id": sender_id,
        "receiver_id": receiver_id,
        "text": text_msg
    })

    conn.commit()

    return jsonify({"status": "success"})

@app.route('/get_chat', methods=['GET'])
def get_chat():
    user1 = request.args.get('user1')
    user2 = request.args.get('user2')

    sql = text("""
        SELECT *
        FROM chat
        WHERE (sender_id = :u1 AND receiver_id = :u2)
            OR (sender_id = :u2 AND receiver_id = :u1)
    """)

    result = conn.execute(sql, {
        "u1": user1,
        "u2": user2
    }).mappings().all()

    return jsonify(result)

@app.route('/update_product', methods = ['POST']) #Handles sending updated informartion 
def update_product():
    return render_template('products.html')

@app.route('/delete_product', methods = ['POST']) #Handles deleting the product 
def delete_product():
    return render_template('products.html')

@app.route('/cart', methods = ['GET', 'POST']) #Handles grabbing all the cart infrmation and sending the order to the admins
def cart_page():
    return render_template('cart.html')

@app.route('/account', methods = ['GET', 'POST']) #Handles getting the account info and sending new info if you chnage something in the account
def account_page():
    if 'username' not in session:
        return redirect(url_for('login_register'))
    
    username = session['username']

    if request.method == 'POST':
        sql = text("""
            SELECT username, password, email_address, first_name, last_name, role
            FROM accounts
            WHERE username = :Username
        """)
        user = conn.execute(sql, {'Username': username}).mappings().fetchone()
        
        new_username = request.form.get('account_username')
        new_password = request.form.get('account_password')
        new_email = request.form.get('account_email')
        new_first = request.form.get('account_first_name')
        new_last = request.form.get('account_last_name')

        if new_password:
            hashed_password = generate_password_hash(new_password)
        else:
            hashed_password = user['password']

        sql = text("""
            UPDATE accounts
            SET username = :Username,
                password = :Password,
                email_address = :Email,
                first_name = :First,
                last_name = :Last
            WHERE username = :CurrentUsername
        """)

        conn.execute(sql, {
            'Username': new_username,
            'Password': hashed_password,
            'Email': new_email,
            'First': new_first,
            'Last': new_last,
            'CurrentUsername': username
        })
        conn.commit()

        session['username'] = new_username

        return redirect(url_for('account_page'))
    
    sql = text("""
        SELECT username, password, email_address, first_name, last_name, role
        From accounts
        WHERE username = :Username
    """)

    user = conn.execute(sql, {'Username': username}).mappings().fetchone()

    return render_template('account.html', user=user)

@app.route('/admin_complaint', methods = ['GET', 'POST']) #Handles getting the reviews/complaints and sending the repsonse back to the customer
def admin_complaint_page():
    return render_template('adminComplaint.html')

@app.route('/vendor_chat', methods = ['GET', 'POST']) #Handles getting the the users and their chats and the vendor sending the chat back
def vendor_chat_page():
    vendors = conn.execute(
        text("SELECT account_id, username FROM accounts WHERE role = 'user'")
    ).fetchall()
    return render_template('vendorChat.html')

@app.route('/admin_confirm_order', methods = ['GET', 'POST']) #Handles getting the orders and their info and sends backs the info for when the admin confirms it or denys it 
def admin_confirm_order_page():
    return render_template('adminConfirmOrder.html')

@app.route('/feedback') 
def feedback_page():
    return render_template('feedback.html') 

if __name__ == '__main__':
    app.run(debug=True)