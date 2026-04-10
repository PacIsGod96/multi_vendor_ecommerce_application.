CREATE DATABASE multi_vendor_ecommerce;
USE multi_vendor_ecommerce;

CREATE TABLE accounts (
	account_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    email_address VARCHAR(50) UNIQUE NOT NULL,
    role enum('vendor', 'user', 'admin') NOT NULL
);

ALTER TABLE accounts
MODIFY last_name VARCHAR(50);

CREATE TABLE product (
	product_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    images JSON
);

CREATE TABLE product_sizes (
	product_id INT NOT NULL,
    size VARCHAR(10) NOT NULL,
    PRIMARY KEY (product_id, size),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE product_colors (
	product_id INT NOT NULL,
    color VARCHAR(30) NOT NULL,
    PRIMARY KEY (product_id, color),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE vendor_product (
	vendor_id INT NOT NULL,
    product_id INT NOT NULL,
	price DECIMAL(10, 2) NOT NULL,
    available_inventory INT NOT NULL,
    PRIMARY KEY (vendor_id, product_id),
    FOREIGN KEY (vendor_id) REFERENCES accounts(account_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

ALTER TABLE vendor_product
DROP COLUMN warranty_period;

CREATE TABLE vendor_product_sizes (
	vendor_id INT NOT NULL,
    product_id INT NOT NULL,
    size VARCHAR(10) NOT NULL,
    PRIMARY KEY (vendor_id, product_id, size),
    FOREIGN KEY (vendor_id, product_id) REFERENCES vendor_product(vendor_id, product_id)
);

CREATE TABLE vendor_product_colors (
	vendor_id INT NOT NULL,
	product_id INT NOT NULL,
    color VARCHAR(20) NOT NULL,
    PRIMARY KEY (vendor_id, product_id, color),
    FOREIGN KEY (vendor_id, product_id) REFERENCES vendor_product(vendor_id, product_id)
);

CREATE TABLE review (
	review_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
	name VARCHAR(50) NOT NULL,
    description TEXT  NOT NULL,
    stars INT NOT NULL,
    date DATE NOT NULL,
    image JSON,
    account_id INT NOT NULL,
    product_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE chat (
	chat_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    text TEXT,
    images JSON,
    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE cart (
	cart_item_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    account_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE orders (
	order_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    account_id INT NOT NULL,
    date DATE NOT NULL,
    status ENUM('pending', 'confirmed', 'shipped', 'handed off') NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE returns (
	return_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    date DATE NOT NULL,
    status ENUM('pending', 'processing', 'complete', 'rejected', 'confirmed') NOT NULL,
    account_id INT NOT NULL,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);

CREATE TABLE warranty (
	warranty_id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT NOT NULL,
    product_id INT NOT NULL,
    duration_months INT NOT NULL,
    description TEXT,
    type ENUM ('manufacturer', 'vendor', 'extended'),
    FOREIGN KEY (vendor_id, product_id) REFERENCES vendor_product(vendor_id, product_id)
);

CREATE TABLE discounts (
	discount_id INT PRIMARY KEY AUTO_INCREMENT,
    vendor_id INT NOT NULL,
    code varchar(50),
    percent_off DECIMAL(5, 2),
    amount_off DECIMAL(10, 2),
    start_date DATE,
    end_date DATE,
    active BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (vendor_id) REFERENCES accounts(account_id)
);

CREATE TABLE discount_product (
	discount_id INT,
    vendor_id INT,
    product_id INT,
    PRIMARY KEY (discount_id, vendor_id, product_id),
    FOREIGN KEY (discount_id) REFERENCES discounts(discount_id),
    FOREIGN KEY (vendor_id, product_id) REFERENCES vendor_product(vendor_id, product_id)
);

-- Logan-- 
INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES
('Bob', 'Target', 'BobTarget', 'password', 'BobT@robmail.com', 'admin'),
('John', 'Walmart', 'JohnWalmart', 'Password', 'JohnW@robmail.com', 'admin');

INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES
('Logan', 'Burkey', 'LoganBurkey', 'password', 'logan@robmail.com', 'user'),
('Jackson', 'Patton', 'JacksonPatton', 'password', 'Jackson@robmail.com', 'user'),
('Collin', 'Williams', 'CollinWilliams', 'password', 'Colin@robmail.com', 'user'),
('Rob', 'Wiley', 'RobWiley', 'password', 'rob@robmail.com', 'user'),
('The', 'Moy', 'TheMoy', 'password', 'Moy@robmail.com', 'user');

INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES
('Tech', 'World', 'TechWorld', 'password', 'tech@robmail.com', 'vendor'),
('Home', 'Essentials', 'HomeEssentials', 'password', 'home@robmail.com', 'vendor'),
('Gadget', 'Pro', 'GadgetPro', 'password', 'gadget@robmail.com', 'vendor');

INSERT INTO product (name, description, images) VALUES
('Wireless Mouse', 'Ergonomic 2.4GHz wireless mouse with adjustable DPI.', JSON_ARRAY('mouse1.jpg')),
('Mechanical Keyboard', 'RGB backlit mechanical keyboard with blue switches.', JSON_ARRAY('keyboard1.jpg')),
('USB-C Cable', 'Durable 1m USB-C to USB-A cable.', JSON_ARRAY('usbc1.jpg')),
('Ceramic Mug', '12oz ceramic mug, microwave and dishwasher safe.', JSON_ARRAY('mug1.jpg')),
('Kitchen Knife Set', '5-piece stainless steel kitchen knife set.', JSON_ARRAY('knives1.jpg')),
('Cutting Board', 'Bamboo cutting board with juice groove.', JSON_ARRAY('board1.jpg')),
('Bluetooth Speaker', 'Portable Bluetooth speaker with 10-hour battery life.', JSON_ARRAY('speaker1.jpg')),
('Smartwatch', 'Fitness tracking smartwatch with heart rate monitor.', JSON_ARRAY('watch1.jpg')),
('Phone Stand', 'Adjustable aluminum phone stand for desk.', JSON_ARRAY('stand1.jpg')),
('Portable Charger', '10,000mAh power bank with fast charging.', JSON_ARRAY('charger1.jpg'));

INSERT INTO vendor_product (vendor_id, product_id, price, available_inventory) VALUES
(8, 1, 25.99, 50),
(8, 2, 79.99, 40),
(8, 3, 9.99, 200),

(9, 4, 12.99, 100),
(9, 5, 49.99, 30),
(9, 6, 19.99, 60),

(10, 7, 39.99, 70),
(10, 8, 129.99, 25),
(10, 9, 14.99, 150),
(10,10, 29.99, 80);

INSERT INTO product_sizes (product_id, size) VALUES
(1, 'M'),
(2, 'L'),
(4, 'SM'),
(5, 'XL'),
(7, 'XXL'),
(8, 'L'),
(10, 'SM');

INSERT INTO product_colors (product_id, color) VALUES
(1, 'Black'),
(2, 'Black'),
(4, 'White'),
(4, 'Blue'),
(5, 'Silver'),
(7, 'Red'),
(7, 'Black'),
(8, 'Black'),
(9, 'Silver'),
(10, 'Black');

INSERT INTO cart (account_id, product_id, quantity) VALUES
(3, 1, 1),
(3, 8, 1),

(4, 4, 2),
(4, 7, 1),

(5, 2, 1),
(5, 10, 2);

INSERT INTO orders (account_id, date, status, total_price) VALUES
(3, '2026-04-05', 'pending',   25.99),
(3, '2026-04-06', 'confirmed', 155.98),
(4, '2026-04-07', 'shipped',   65.97),
(4, '2026-04-08', 'shipped',   129.99),
(5, '2026-04-09', 'handed off',159.97),
(5, '2026-04-10', 'pending',   79.99),
(6, '2026-04-11', 'shipped',   69.98);

INSERT INTO discounts (vendor_id, code, percent_off, start_date, end_date) VALUES
(8, 'DISC10', 10.00, NULL, NULL),
(9, 'DISC15', 15.00, NULL, NULL),
(10, 'DISC20', 20.00, '2026-04-01', '2026-04-30'),
(10, 'DISC25', 25.00, '2026-04-10', '2026-04-20');

INSERT INTO discount_product (discount_id, vendor_id, product_id) VALUES
(1, 8, 1),
(1, 8, 2),

(2, 9, 4),
(2, 9, 5),

(3, 10, 7),
(3, 10, 8),

(4, 10, 9),
(4, 10, 10);

- #5: "?" will be new value being checked - 
SELECT * FROM accounts WHERE username IS NOT NULL;
INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES ('user', 'create', 'createUser', 'pw', 'email', 'user');
SELECT * FROM accounts WHERE username = "LoganBurkey" AND password = "password";
SELECT * FROM accounts WHERE email_address = "logan@robmail.com" AND password = "password";
INSERT INTO product (name, description, images) VALUES ('product', 'description', 'image');
INSERT INTO vendor_product (vendor_id, product_id, price, available_inventory) VALUES (8, 69, 20, 200);
UPDATE product SET name = 'product1', description = 'new', images = 'image1' WHERE product_id = 1;
UPDATE vendor_product SET price = 70, available_inventory = 180 WHERE vendor_id = 8 AND product_id = 69;
DELETE FROM product WHERE product_id = 69;
SELECT * FROM product WHERE name LIKE CONCAT('%', ?, '%');
SELECT * FROM product WHERE description LIKE CONCAT('%', ?, '%');
SELECT product.* FROM product JOIN vendor_product  ON product.product_id = vendor_product.product_id WHERE vendor_product.vendor_id = 1;
SELECT product.* FROM product JOIN product_colors ON product.product_id = product_colors.product_id WHERE product_colors.color = 1;
SELECT product.* FROM product JOIN product_sizes ON product.product_id = product_sizes.product_id WHERE product_sizes.size = 'large';
SELECT product.*, vendor_product.available_inventory
FROM product JOIN vendor_product ON product.product_id = vendor_product.product_id WHERE vendor_product.available_inventory > 0;
INSERT INTO cart (account_id, product_id, quantity) VALUES (1, 69, 4);
SELECT * FROM cart WHERE account_id = 1;
UPDATE cart SET quantity = 10 WHERE cart_item_id = 1;
DELETE FROM cart WHERE cart_item_id = 1;
CREATE TABLE wishlist (
    wishlist_id INT AUTO_INCREMENT PRIMARY KEY,
    account_id INT,
    product_id INT,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);
INSERT INTO wishlist (account_id, product_id) VALUES (1, 69);
SELECT * FROM wishlist WHERE account_id = 1;
DELETE FROM wishlist WHERE wishlist_id = 1;
INSERT INTO orders (account_id, date, status, total_price) VALUES (?, CURDATE(), 'pending', ?);
UPDATE orders SET status = 'confirmed' WHERE order_id = 1;
UPDATE orders SET status = ? WHERE order_id = 1;
SELECT SUM(vendor_product.price * cart.quantity) AS total_price FROM cart JOIN vendor_product ON cart.product_id = vendor_product.product_id WHERE cart.account_id = 1;
INSERT INTO review (name, description, stars, date, account_id, product_id) VALUES ("review", "description", 5, CURDATE(), 1, 69);
SELECT * FROM review WHERE product_id = 69;
SELECT * FROM review WHERE account_id = 1;
SELECT * FROM review ORDER BY date DESC;
SELECT * FROM review ORDER BY stars DESC;
UPDATE review SET description = 'desc', stars = 4 WHERE review_id = 1;
DELETE FROM review WHERE review_id = ?;
INSERT INTO returns (name, description, date, status, account_id) VALUES ('name', 'desc', CURDATE(), 'pending', 1);
UPDATE returns SET status = 'pending' WHERE return_id = 1;
SELECT * FROM returns WHERE account_id = 1;
SELECT warranty.*, orders.date AS purchase_date, DATE_ADD(orders.date, INTERVAL warranty.duration_months MONTH) AS expiry_date FROM warranty JOIN orders ON orders.account_id = ? WHERE warranty.product_id = ? HAVING CURDATE() <= expiry_date;
INSERT INTO chat (text, images, account_id) VALUES ('text', 'img', 1);
SELECT * FROM chat WHERE account_id = 1;
DELETE FROM chat WHERE chat_id = 1;
