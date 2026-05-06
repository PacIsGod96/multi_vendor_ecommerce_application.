from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from sqlalchemy import create_engine, text, bindparam
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)

app.secret_key = app.secret_key = "JohnWalmart"

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
        SELECT account_id, username, password, role
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
            session['user_id'] = result['account_id']
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

@app.route('/products', methods=['GET'])
def products_page():

    rows = conn.execute(text("""
        SELECT 
            p.product_id,
            p.name,
            p.vendor,
            p.price,
            a.username AS vendor_name,
            pi.image_path
        FROM product p
        LEFT JOIN product_images pi 
            ON p.product_id = pi.product_id
        LEFT JOIN accounts a
            ON p.vendor = a.account_id
    """)).mappings().all()

    sizes_rows = conn.execute(text("""
        SELECT product_id, size FROM product_sizes
    """)).mappings().all()

    colors_rows = conn.execute(text("""
        SELECT product_id, color FROM product_colors
    """)).mappings().all()

    vendors = conn.execute(
        text("SELECT account_id, username FROM accounts WHERE role = 'vendor'")
    ).mappings().all()

    products_dict = {}

    for row in rows:
        pid = row["product_id"]

        if pid not in products_dict:
            products_dict[pid] = {
                "product_id": pid,
                "name": row["name"],
                "price": row["price"],
                "vendor": row["vendor_name"],
                "vendor_id": row["vendor"],
                "images": [],
                "sizes": [],
                "colors": []
            }

        if row["image_path"]:
            products_dict[pid]["images"].append(row["image_path"])

    for s in sizes_rows:
        pid = s["product_id"]
        if pid in products_dict:
            products_dict[pid]["sizes"].append(s["size"])

    for c in colors_rows:
        pid = c["product_id"]
        if pid in products_dict:
            products_dict[pid]["colors"].append(c["color"])

    products = list(products_dict.values())

    for p in products:
        if not p["images"]:
            p["images"] = ["Images/default.png"]

    return render_template(
        "products.html",
        products=products,
        vendors=vendors,
        products_json=json.dumps(products)
    )

@app.route('/get_inbox', methods=['GET'])
def get_inbox():
    user_id = session.get('user_id')

    print("INBOX USER ID:", user_id)

    if not user_id:
        return jsonify([])

    sql = text("""
        SELECT
            a.account_id,
            a.username,
            MAX(c.chat_id) as last_message_id
        FROM chat c
        JOIN accounts a
            ON a.account_id =
                CASE
                    WHEN c.sender_id = :uid THEN c.receiver_id
                    ELSE c.sender_id
                END
        WHERE c.sender_id = :uid OR c.receiver_id = :uid
        GROUP BY a.account_id, a.username
    """)

    result = conn.execute(sql, {"uid": user_id}).mappings().all()

    inbox = [dict(row) for row in result]

    return jsonify(inbox)

@app.route('/get_chat', methods=['GET'])
def get_chat():
    user1 = int(request.args.get('user1'))
    user2 = int(request.args.get('user2'))

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

    return jsonify([dict(r) for r in result])

@app.route('/send_chat', methods=['POST'])
def send_chat():
    data = request.get_json()
    
    sender_id = int(data['sender_id'])
    receiver_id = int(data['receiver_id'])
    text_msg = data['text']

    sql = text("""
        INSERT INTO chat (sender_id, receiver_id, text)
        VALUES (:sender_id, :receiver_id, :text)
    """)

    with engine.begin() as conn:
        conn.execute(sql, {
            "sender_id": sender_id,
            "receiver_id": receiver_id,
            "text": text_msg
        })

    return jsonify({"status": "success"})

@app.route('/add_product', methods=['POST'])
def add_product():

    if 'user_id' not in session:
        return redirect(url_for('login_register'))

    name = request.form.get('name')
    price = request.form.get('price')
    sizes = request.form.getlist('sizes')
    colors = request.form.getlist('colors')
    images = request.form.getlist('images')  

    vendor = request.form.get('vendor')

    
    result = conn.execute(text("""
        INSERT INTO product (name, vendor, price)
        VALUES (:name, :vendor, :price)
    """), {
        'name': name,
        'vendor': vendor,
        'price': price
    })

    product_id = result.lastrowid

    
    for size in sizes:
        conn.execute(text("""
            INSERT INTO product_sizes (product_id, size)
            VALUES (:pid, :size)
        """), {
            'pid': product_id,
            'size': size
        })


    for color in colors:
        if color.strip():
            conn.execute(text("""
                INSERT INTO product_colors (product_id, color)
                VALUES (:pid, :color)
            """), {
                'pid': product_id,
                'color': color
            })

    import os

    for img in images:
        if img.strip():
            filename = os.path.basename(img)  
            path = f"Images/{filename}"       

            conn.execute(text("""
                INSERT INTO product_images (product_id, image_path)
                VALUES (:pid, :path)
            """), {
                'pid': product_id,
                'path': path
            })

    conn.commit()
    return redirect(url_for('products_page'))

@app.route('/update_product', methods=['POST'])
def update_product():
    if 'user_id' not in session:
        return redirect(url_for('login_register'))

    product_id_raw = request.form.get('product_id')
    user_role = session.get('role')
    user_id = session.get('user_id')

    print(f"DEBUG: Received product_id_raw = '{product_id_raw}' (type: {type(product_id_raw)})")
    print(f"DEBUG: Logged in user_id = {user_id}, role = {user_role}")
    
    if not product_id_raw or not product_id_raw.strip():
        return "Error: product_id is missing or empty in the form submission!", 400

    try:
        product_id = int(product_id_raw)
    except ValueError:
        return f"Error: product_id '{product_id_raw}' is not a valid number!", 400

    owner_check = conn.execute(text("""
        SELECT vendor FROM product WHERE product_id = :pid
    """), {'pid': product_id}).mappings().fetchone()

    print(f"DEBUG: Database owner_check result = {owner_check}")

    if not owner_check:
        return f"Product not found (Searched for product_id: {product_id})", 404

    if user_role != 'admin' and owner_check['vendor'] != user_id:
        return "Unauthorized", 403

    name = request.form.get('name')
    price = request.form.get('price')
    sizes = request.form.getlist('sizes')
    colors = request.form.getlist('colors')
    images = request.form.getlist('images')

    if name and name.strip():
        conn.execute(text("""
            UPDATE product
            SET name = :name
            WHERE product_id = :pid
        """), {'name': name, 'pid': product_id})

    if price and price.strip():
        conn.execute(text("""
            UPDATE product
            SET price = :price
            WHERE product_id = :pid
        """), {'price': price, 'pid': product_id})

    if sizes:
        conn.execute(text("""
            DELETE FROM product_sizes
            WHERE product_id = :pid
        """), {'pid': product_id})
        
        for size in sizes:
            if size.strip():
                conn.execute(text("""
                    INSERT INTO product_sizes (product_id, size)
                    VALUES (:pid, :size)
                """), {'pid': product_id, 'size': size})

    active_colors = [c.strip() for c in colors if c.strip()]
    if active_colors:
        conn.execute(text("""
            DELETE FROM product_colors
            WHERE product_id = :pid
        """), {'pid': product_id})

        for color in active_colors:
            conn.execute(text("""
                INSERT INTO product_colors (product_id, color)
                VALUES (:pid, :color)
            """), {'pid': product_id, 'color': color})

    active_images = [img.strip() for img in images if img.strip()]
    if active_images:
        conn.execute(text("""
            DELETE FROM product_images
            WHERE product_id = :pid
        """), {'pid': product_id})

        for img in active_images:
            filename = os.path.basename(img)
            path = f"Images/{filename}"
            conn.execute(text("""
                INSERT INTO product_images (product_id, image_path)
                VALUES (:pid, :path)
            """), {'pid': product_id, 'path': path})

    conn.commit()
    return redirect(url_for('products_page'))

@app.route('/delete_product', methods=['POST'])
def delete_product():

    if 'user_id' not in session:
        return redirect(url_for('login_register'))

    product_id = request.form.get('product_id')
    role = session.get('role')

    if not product_id:
        return "Missing product_id", 400

    if role not in ['admin', 'vendor']:
        return "Unauthorized", 403

    if role == 'vendor':
        owner = conn.execute(text("""
            SELECT vendor FROM product WHERE product_id = :pid
        """), {'pid': product_id}).mappings().fetchone()

        if not owner or owner['vendor'] != session.get('user_id'):
            return "Not your product", 403

    conn.execute(text("""
        DELETE FROM product_images WHERE product_id = :pid
    """), {'pid': product_id})

    conn.execute(text("""
        DELETE FROM product_sizes WHERE product_id = :pid
    """), {'pid': product_id})

    conn.execute(text("""
        DELETE FROM product_colors WHERE product_id = :pid
    """), {'pid': product_id})

    conn.execute(text("""
        DELETE FROM product WHERE product_id = :pid
    """), {'pid': product_id})

    conn.commit()

    return redirect(url_for('products_page'))


@app.route('/cart', methods = ['GET', 'POST']) 
def cart_page():
    return render_template('cart.html')

@app.route('/account', methods = ['GET', 'POST'])
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

@app.route('/admin_complaint', methods = ['GET', 'POST']) 
def admin_complaint_page():
    return render_template('adminComplaint.html')

@app.route('/vendor_chat', methods=['GET', 'POST'])
def vendor_chat_page():
    vendors = conn.execute(
        text("SELECT account_id, username FROM accounts WHERE role = 'vendor'")
    ).fetchall()

    return render_template('vendorChat.html', vendors=vendors)

@app.route('/admin_confirm_order', methods=['GET', 'POST'])
def admin_confirm_order_page():
    if request.method == 'POST':
        order_id = request.form.get('order_id')
        sql = text("UPDATE orders SET status = 'confirmed' WHERE order_id = :oid")
        conn.execute(sql, {"oid": order_id})
        conn.commit()
        return "Success", 200
    orders_query = text("""
        SELECT order_id, account_id, date, total_price 
        FROM orders 
        WHERE status = 'pending'
    """)
    orders = conn.execute(orders_query).mappings().fetchall()

    return render_template('adminConfirmOrder.html', orders=orders)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        category = request.form.get('category')
        username = session.get('username')

        user_res = conn.execute(text("SELECT account_id FROM accounts WHERE username = :u"), {"u": username}).mappings().fetchone()
        account_id = user_res['account_id'] if user_res else None

        if category == 'Review':
            sql = text("""
                INSERT INTO review (name, description, stars, date, account_id, product_id)
                VALUES (:name, :desc, :stars, CURDATE(), :uid, :pid)
            """)
            conn.execute(sql, {
                'name': f"Review by {username}",
                'desc': request.form.get('review_text'),
                'stars': request.form.get('rating'),
                'uid': account_id,
                'pid': request.form.get('product_id')
            })

        elif category == 'Refund':
            sql = text("""
                INSERT INTO returns (name, description, date, status, account_id)
                VALUES (:name, :desc, CURDATE(), 'pending', :uid)
            """)
            conn.execute(sql, {
                'name': f"Return Request - Order {request.form.get('order_id')}",
                'desc': request.form.get('review_text'),
                'uid': account_id
            })

        elif category == 'Complaint':
            print(f"Complaint received from {username}: {request.form.get('review_text')}")

        conn.commit()
        return redirect(url_for('feedback_page'))

    return render_template('feedback.html')

@app.route('/vendor_chat')
def vendor_chat():
    return render_template('vendorChat.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/create_order', methods=['POST'])
def create_order():
    account_id = request.form.get('account_id')
    total_price = request.form.get('total_price')

    sql = text("""
        INSERT INTO orders (account_id, date, status, total_price)
        VALUES (:account_id, CURDATE(), 'pending', :total_price)
    """)

    conn.execute(sql, {
        "account_id": account_id,
        "total_price": total_price
    })
    conn.commit()

    return jsonify({"status": "order_created"}), 200


# ⬇️ THIS MUST ALWAYS BE LAST ⬇️
if __name__ == "__main__":
    app.run(debug=True)
