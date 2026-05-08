from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from sqlalchemy import create_engine, text, bindparam
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json

app = Flask(__name__)

app.secret_key = os.urandom(24)

conn_str = "mysql://root:cset155@localhost/multi_vendor_ecommerce"
engine = create_engine(conn_str, echo=True)

@app.route('/template')
def view_template():
    return render_template("template.html")

#----------------------------------------------Backend for login/register and account-------------------------------------------------------
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
    with engine.begin() as conn:
        conn.execute(sql, {
            'FirstName': first_name,
            'LastName': last_name,
            'Username': username,
            'Password': generate_password_hash(password),
            'EmailAddress': email,
            'Role': role
        })

    return render_template('index.html')

@app.route('/login', methods = ['POST']) 
def login():
    username = request.form.get('login_username')
    password = request.form.get('login_password')

    # 1. Fetch account_id along with other details
    sql = text("""
        SELECT account_id, username, password, role
        FROM accounts
        WHERE username = :Username
    """)
    with engine.connect() as conn:
        result = conn.execute(sql, {'Username': username}).mappings().fetchone()

    if result:
        stored_password = result['password']
        role = result['role']

        if check_password_hash(stored_password, password):
            # 2. Store the correct key ('user_id') in the session
            session['user_id'] = result['account_id'] 
            session['username'] = result['username']
            session['role'] = role

            return redirect(url_for('products_page'))
        else: 
            return "Incorrect password", 401
    else:
        return "Username not found", 404

@app.route('/logout', methods = ['GET']) #Handles loging out
def logout():
    session.clear()
    return redirect(url_for('login_register'))

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

        with engine.connect() as conn:
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
        with engine.begin() as conn:
            conn.execute(sql, {
                'Username': new_username,
                'Password': hashed_password,
                'Email': new_email,
                'First': new_first,
                'Last': new_last,
                'CurrentUsername': username
            })

        session['username'] = new_username

        return redirect(url_for('account_page'))
    
    sql = text("""
        SELECT username, password, email_address, first_name, last_name, role
        From accounts
        WHERE username = :Username
    """)

    with engine.connect() as conn:
        user = conn.execute(sql, {'Username': username}).mappings().fetchone()

    return render_template('account.html', user=user)
#-----------------------------------------------------------End of backend for login/register and account------------------------------------------

#--------------------------------------------------Backend for products-----------------------------------------------------------------------
@app.route('/products', methods=['GET'])
def products_page():
    # 1. Get the filter from the URL (if it exists)
    selected_vendor = request.args.get('vendor')
    search_text = request.args.get('search')

    with engine.connect() as conn:
        # 2. Build the Product Query
        # We use a base query and append a WHERE clause if a filter is active
        product_sql = """
            SELECT 
                p.product_id, p.name, p.vendor, p.price,
                a.username AS vendor_name, pi.image_path
            FROM product p
            LEFT JOIN product_images pi ON p.product_id = pi.product_id
            LEFT JOIN accounts a ON p.vendor = a.account_id
        """
        
        filters = []
        params = {}

        if selected_vendor:
            filters.append("p.vendor = :v_id")
            params['v_id'] = selected_vendor

        if search_text:
            filters.append("p.name LIKE :search")
            params['search'] = f"%{search_text}%"

        if filters:
            product_sql += " WHERE " + " AND ".join(filters)

        rows = conn.execute(text(product_sql), params).mappings().all()

        # Fetch sizes
        sizes_sql = """
            SELECT ps.product_id, ps.size
            FROM product_sizes ps
            JOIN product p ON ps.product_id = p.product_id
        """

        # Fetch colors
        colors_sql = """
            SELECT pc.product_id, pc.color
            FROM product_colors pc
            JOIN product p ON pc.product_id = p.product_id
        """

        if filters:
            where_clause = " WHERE " + " AND ".join(filters)

            sizes_sql += where_clause
            colors_sql += where_clause

        sizes_rows = conn.execute(text(sizes_sql), params).mappings().all()
        colors_rows = conn.execute(text(colors_sql), params).mappings().all()

        # 3. Get all vendors for the dropdown menu
        vendors = conn.execute(
            text("SELECT account_id, username FROM accounts WHERE role = 'vendor'")
        ).mappings().all()

    # 4. Data Structuring (Organizing rows into a dictionary)
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

    # 5. Final Formatting
    products = list(products_dict.values())

    for p in products:
        if not p["images"]:
            p["images"] = ["Images/default.png"]

    # 6. Render with the new 'selected_vendor' variable
    return render_template(
        "products.html",
        products=products,
        vendors=vendors,
        products_json=json.dumps(products),
        selected_vendor=selected_vendor
    )

@app.route('/add_product', methods=['POST'])
def add_product():
    # 1. Identity & Role Check
    current_user_id = session.get('user_id')
    role = session.get('role')

    if not current_user_id or role not in ['vendor', 'admin']:
        return "Unauthorized: Please log in as a vendor or admin", 401

    # 2. Assign Vendor Ownership
    # If Admin, use the ID from the form dropdown. 
    # If Vendor, force the ID to be their own session ID for security.
    if role == 'admin':
        vendor_id = request.form.get('vendor')
    else:
        vendor_id = current_user_id

    if not vendor_id:
        return "Error: No vendor assigned to product", 400

    # 3. Collect Form Data
    name = request.form.get('name')
    price = request.form.get('price')
    sizes = request.form.getlist('sizes')
    colors = request.form.getlist('colors')
    images = request.files.getlist('images')

    # Ensure image directory exists
    os.makedirs(os.path.join('static', 'Images'), exist_ok=True)

    try:
        with engine.begin() as conn:
            # 4. Insert into 'product' table
            result = conn.execute(text("""
                INSERT INTO product (name, vendor, price)
                VALUES (:name, :vendor_id, :price)
            """), {
                'name': name,
                'vendor_id': vendor_id,
                'price': price
            })
            
            # Get the ID of the product we just created
            product_id = result.lastrowid

            # 5. Insert Sizes
            for size in sizes:
                if size.strip():
                    conn.execute(text("""
                        INSERT INTO product_sizes (product_id, size)
                        VALUES (:pid, :size)
                    """), {'pid': product_id, 'size': size})

            # 6. Insert Colors
            for color in colors:
                if color.strip():
                    conn.execute(text("""
                        INSERT INTO product_colors (product_id, color)
                        VALUES (:pid, :color)
                    """), {'pid': product_id, 'color': color})

            # 7. Handle Image Uploads
            for image in images:
                if image and image.filename:
                    # Create a unique filename to prevent overwriting
                    image_path = f"Images/{product_id}_{image.filename}"
                    full_path = os.path.join('static', image_path)
                    image.save(full_path)
                    
                    conn.execute(text("""
                        INSERT INTO product_images (product_id, image_path)
                        VALUES (:pid, :path)
                    """), {'pid': product_id, 'path': image_path})

        return redirect(url_for('products_page'))

    except Exception as e:
        print(f"Error adding product: {e}")
        return "A database error occurred.", 500


@app.route('/update_product', methods=['POST'])
def update_product():
    if 'user_id' not in session:
        return "Unauthorized", 401

    product_id = request.form.get('product_id')
    name = request.form.get('name')
    price = request.form.get('price')
    sizes = request.form.getlist('sizes')
    colors = request.form.getlist('colors')
    images = request.files.getlist('images')

    # --- OWNERSHIP CHECK ---
    with engine.connect() as conn:
        product = conn.execute(text("""
            SELECT vendor FROM product WHERE product_id = :pid
        """), {'pid': product_id}).mappings().fetchone()

    if not product:
        return "Product not found", 404

    # Fix: Force both values to integers to ensure the comparison works
    try:
        current_user_id = int(session.get('user_id'))
        product_owner_id = int(product['vendor'])
    except (TypeError, ValueError):
        return "Unauthorized: Invalid user or product data", 401

    is_admin = session.get('role') == 'admin'
    is_owner = product_owner_id == current_user_id

    if not (is_admin or is_owner):
        return f"Unauthorized: This product belongs to Vendor ID {product_owner_id}", 403
    # -----------------------

    os.makedirs(os.path.join('static', 'Images'), exist_ok=True)

    with engine.begin() as conn:
        # Update core details
        conn.execute(text("""
            UPDATE product
            SET name = :name, price = :price
            WHERE product_id = :pid
        """), {'name': name, 'price': price, 'pid': product_id})

        # Refresh attributes (Delete then Re-insert)
        conn.execute(text("DELETE FROM product_sizes WHERE product_id = :pid"), {'pid': product_id})
        conn.execute(text("DELETE FROM product_colors WHERE product_id = :pid"), {'pid': product_id})

        for size in sizes:
            if size.strip():
                conn.execute(text("INSERT INTO product_sizes (product_id, size) VALUES (:pid, :size)"), 
                             {'pid': product_id, 'size': size})

        for color in colors:
            if color.strip():
                conn.execute(text("INSERT INTO product_colors (product_id, color) VALUES (:pid, :color)"), 
                             {'pid': product_id, 'color': color})

        # Handle Images only if new ones were uploaded
        if any(img and img.filename for img in images):
            conn.execute(text("DELETE FROM product_images WHERE product_id = :pid"), {'pid': product_id})
            for image in images:
                if image and image.filename:
                    image_path = f"Images/{product_id}_{image.filename}"
                    image.save(os.path.join('static', image_path))
                    conn.execute(text("INSERT INTO product_images (product_id, image_path) VALUES (:pid, :path)"), 
                                 {'pid': product_id, 'path': image_path})

    return redirect(url_for('products_page'))


@app.route('/delete_product', methods=['POST'])
def delete_product():
    user_id = session.get('user_id')
    role = session.get('role')
    
    if not user_id:
        return "Unauthorized", 401

    product_id = request.form.get('product_id')

    with engine.connect() as conn:
        product = conn.execute(text("SELECT vendor FROM product WHERE product_id = :pid"), 
                               {'pid': product_id}).mappings().fetchone()

    if not product:
        return "Product not found", 404

    # Verification Logic
    if role != 'admin' and product['vendor'] != user_id:
        return "Unauthorized: You cannot delete products that aren't yours", 403

    with engine.begin() as conn:
        conn.execute(text("DELETE FROM product_images WHERE product_id = :pid"), {'pid': product_id})
        conn.execute(text("DELETE FROM product_sizes WHERE product_id = :pid"), {'pid': product_id})
        conn.execute(text("DELETE FROM product_colors WHERE product_id = :pid"), {'pid': product_id})
        conn.execute(text("DELETE FROM product WHERE product_id = :pid"), {'pid': product_id})

    return redirect(url_for('products_page'))

#---------------------------------------------End of backend for products------------------------------------------------------------

#--------------------------------------------Backend for cart------------------------------------------------------------------------
@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'username' not in session:
        return redirect(url_for('login_register'))

    product_id = request.form.get('product_id')
    size = request.form.get('size')
    color = request.form.get('color')
    quantity = int(request.form.get('quantity', 1))

    username = session['username']

    with engine.connect() as conn:
        user_res = conn.execute(
            text("SELECT account_id FROM accounts WHERE username = :u"),
            {"u": username}
        ).mappings().fetchone()

    account_id = user_res['account_id']

    with engine.begin() as conn:
        existing = conn.execute(
            text("""
                SELECT quantity FROM cart 
                WHERE account_id = :uid AND product_id = :pid 
                AND size = :size AND color = :color
            """),
            {"uid": account_id, "pid": product_id, "size": size, "color": color}
        ).mappings().fetchone()

        if existing:
            conn.execute(
                text("""
                    UPDATE cart 
                    SET quantity = quantity + :qty 
                    WHERE account_id = :uid AND product_id = :pid 
                    AND size = :size AND color = :color
                """),
                {"uid": account_id, "pid": product_id, "qty": quantity, "size": size, "color": color}
            )
        else:
            conn.execute(
                text("""
                    INSERT INTO cart (account_id, product_id, size, color, quantity)
                    VALUES (:uid, :pid, :size, :color, :qty)
                """),
                {"uid": account_id, "pid": product_id, "size": size, "color": color, "qty": quantity}
            )

    return redirect(url_for('cart_page'))



@app.route('/cart', methods=['GET'])
def cart_page():
    if 'username' not in session:
        return redirect(url_for('login_register'))
    
    username = session['username']

    with engine.connect() as conn:
        user_res = conn.execute(
            text("SELECT account_id FROM accounts WHERE username = :u"),
            {"u": username}
        ).mappings().fetchone()

    account_id = user_res['account_id']

    query = text("""
        SELECT 
            p.product_id,
            p.name,
            p.price,
            p.vendor AS vendor_name,
            pi.image_path,
            c.cart_item_id,
            c.quantity
        FROM cart c
        JOIN product p ON c.product_id = p.product_id
        LEFT JOIN product_images pi ON p.product_id = pi.product_id
        WHERE c.account_id = :uid
    """)

    with engine.connect() as conn:
        cart_products = conn.execute(query, {"uid": account_id}).mappings().fetchall()

    total = sum(item['price'] * item['quantity'] for item in cart_products)

    return render_template('cart.html', cart=cart_products, total=total)


#-------------------------------------------------------End of backend for cart-----------------------------------------------------------

#------------------------------------------------------Backend for orders------------------------------------------------------------
@app.route('/create_order', methods=['POST'])
def create_order():
    account_id = request.form.get('account_id')
    total_price = request.form.get('total_price')

    sql = text("""
        INSERT INTO orders (account_id, date, status, total_price)
        VALUES (:account_id, CURDATE(), 'pending', :total_price)
    """)
    with engine.begin() as conn:
        conn.execute(sql, {
            "account_id": account_id,
            "total_price": total_price
        })

    return jsonify({"status": "order_created"}), 200

@app.route('/admin_confirm_order', methods=['GET', 'POST'])
def admin_confirm_order_page():
    if request.method == 'POST':
        order_id = request.form.get('order_id')

        with engine.begin() as conn:
            sql = text("UPDATE orders SET status = 'confirmed' WHERE order_id = :oid")
            conn.execute(sql, {"oid": order_id})
        return "Success", 200
    
    with engine.connect() as conn:
        orders_query = text("""
            SELECT order_id, account_id, date, total_price 
            FROM orders 
            WHERE status = 'pending'
        """)
        orders = conn.execute(orders_query).mappings().fetchall()
    orders_query = text("""
        SELECT o.order_id, a.username, o.date, o.total_price 
        FROM orders o
        JOIN accounts a ON o.account_id = a.account_id
        WHERE o.status = 'pending'
    """)

    with engine.connect() as conn:
        orders = conn.execute(orders_query).mappings().fetchall()

    return render_template('adminConfirmOrder.html', orders=orders)
#------------------------------------------------------End of backend for orders---------------------------------------------------------

#-----------------------------------------------------Backend for the chat------------------------------------------------
@app.route('/get_inbox', methods=['GET'])
def get_inbox():
    user_id = session.get('user_id')

    # print("INBOX USER ID:", user_id)

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
    with engine.connect() as conn:
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
        ORDER BY chat_id ASC
    """)
    with engine.connect() as conn:
      result = conn.execute(sql, {
          "u1": user1,
          "u2": user2
      }).mappings().all()

    return jsonify([dict(row) for row in result])

@app.route('/send_chat', methods = ['POST'])
def send_chat():
    data = request.get_json()

    sender_id = data['sender_id']
    receiver_id = data['receiver_id']
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

@app.route('/vendor_chat', methods = ['GET', 'POST'])
def vendor_chat_page():
    with engine.connect() as conn:
        vendors = conn.execute(
            text("SELECT account_id, username FROM accounts WHERE role = 'vendor'")
        ).fetchall()

    return render_template('vendorChat.html', vendors=vendors)

@app.route('/vendor_chat')
def vendor_chat():
    return render_template('vendorChat.html')
#---------------------------------------------------End of backend for chat----------------------------------------------------------

#-----------------------------------------------------Backend for complaints---------------------------------------------------------------
@app.route('/send_review_complaint', methods=['POST'])
def send_review_complaint():
    if 'username' not in session:
        return redirect(url_for('login_register'))

    category = request.form.get('category')
    content = request.form.get('review_text')
    product_id = request.form.get('product_id')
    stars = request.form.get('rating')
    username = session['username']

    with engine.connect() as conn:
        user_res = conn.execute(text("SELECT account_id FROM accounts WHERE username = :u"), {"u": username}).mappings().fetchone()
    account_id = user_res['account_id']

    with engine.begin() as conn:
        if category == 'Review':
            sql = text("""
                INSERT INTO review (name, description, stars, date, account_id, product_id)
                VALUES (:name, :desc, :stars, CURDATE(), :uid, :pid)
            """)
            conn.execute(sql, {
                'name': f"Review by {username}",
                'desc': content,
                'stars': stars,
                'uid': account_id,
                'pid': product_id
            })
        else:
            # Handling for complaints or other feedback types
            print(f"Complaint from {username}: {content}")

    return redirect(url_for('products_page'))

@app.route('/admin_complaint', methods = ['GET', 'POST']) 
def admin_complaint_page():
    return render_template('adminComplaint.html')
#-------------------------------------------------End of backend for complaints----------------------------------------------------------

#------------------------------------------------Backend for feedback---------------------------------------------------------------------
@app.route('/feedback', methods=['GET', 'POST'])
def feedback_page():
    if request.method == 'POST':
        category = request.form.get('category')
        username = session.get('username')
        
        with engine.begin() as conn:
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
#         elif category == 'Refund':
#             sql = text("""
#                 INSERT INTO returns (name, description, date, status, account_id)
#                 VALUES (:name, :desc, CURDATE(), 'pending', :uid)
#             """)
#             conn.execute(sql, {
#                 'name': f"Return Request - Order {request.form.get('order_id')}",
#                 'desc': request.form.get('review_text'),
#                 'uid': account_id
#             })

            # elif category == 'Complaint':
            #     print(f"Complaint received from {username}: {request.form.get('review_text')}")
#         elif category == 'Complaint':
#             print(f"Complaint received from {username}: {request.form.get('review_text')}")

#         conn.commit()
#         return redirect(url_for('feedback_page'))

    return render_template('feedback.html')
#-------------------------------------------------End of backend for feedback-----------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
