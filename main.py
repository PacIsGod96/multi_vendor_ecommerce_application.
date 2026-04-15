from flask import Flask, render_template, request, url_for, redirect, session
from sqlalchemy import create_engine, text, bindparam
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)

conn_str = "mysql://root:cset155@localhost/multi_vendor_ecommerce"
engine = create_engine(conn_str, echo=True)
conn = engine.connect()

@app.route('/template')
def view_template():
    return render_template("template.html")

@app.route('/', methods= ['GET'])
def login_register():
    return render_template("index.html")

@app.route('/', methods = ['POST'])
def register_post():
    return render_template('index.html')

@app.route('/login', methods = ['POST'])
def login():
    return render_template('home.html')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return redirect(url_for('register'))

@app.route('/products', methods = ['GET'])
def products_page():
    return render_template('products.html')

@app.route('/cart', methods = ['GET'])
def cart_page():
    return render_template('cart.html')

@app.route('/account', methods = ['GET'])
def account_page():
    return render_template('account.html')

@app.route('/admin_compliant', methods = ['GET'])
def admin_complaint_page():
    return render_template('adminComplaint.html')

@app.route('/vendor_chat', methods = ['GET'])
def vendor_chat_page():
    return render_template('vendorChat.html')

@app.route('/admin_confirm_order', methods = ['GET'])
def admin_confirm_order_page():
    return render_template('adminConfirmOrder')

if __name__ == '__main__':
    app.run(debug=True)