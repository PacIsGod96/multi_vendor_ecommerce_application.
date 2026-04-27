from flask import Flask, render_template, request, url_for, redirect, session
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
    username = request.form['register_username']
    password = request.form['register_password']
    first_name = request.form['register_first_name']
    last_name = request.form['register_last_name']
    email = request.form['register_email']
    role = request.form['register_role']

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
    username = request.form['login_username']
    password = request.form['login_password']

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

@app.route('/add_product', methods = ['POST'])
def add_product():
    return render_template('products.html')

@app.route('/add_to_cart', methods = ['POST']) #Handles adding the product to the cart
def add_to_cart():
    return render_template('products.html')

@app.route('/send_review_complaint', methods = ['POST']) #Handles sending a review on the product
def send_review_complaint():
    return render_template('products.html')

@app.route('/send_chat', methods = ['POST']) #Hadles sending a chat to the vendor
def send_chat():
    return render_template('products.html')

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
    return render_template('account.html')

@app.route('/admin_complaint', methods = ['GET', 'POST']) #Handles getting the reviews/complaints and sending the repsonse back to the customer
def admin_complaint_page():
    return render_template('adminComplaint.html')

@app.route('/vendor_chat', methods = ['GET', 'POST']) #Handles getting the the users and their chats and the vendor sending the chat back
def vendor_chat_page():
    return render_template('vendorChat.html')

@app.route('/admin_confirm_order', methods = ['GET', 'POST']) #Handles getting the orders and their info and sends backs the info for when the admin confirms it or denys it 
def admin_confirm_order_page():
    return render_template('adminConfirmOrder')

if __name__ == '__main__':
    app.run(debug=True)