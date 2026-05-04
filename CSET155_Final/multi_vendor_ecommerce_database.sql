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

DROP TABLE vendor_product_sizes;
DROP TABLE vendor_product_colors;
ALTER TABLE warranty DROP FOREIGN KEY warranty_ibfk_1;
ALTER TABLE warranty DROP COLUMN vendor_id;
ALTER TABLE warranty
ADD FOREIGN KEY (product_id) REFERENCES product(product_id);
ALTER TABLE discount_product DROP FOREIGN KEY discount_product_ibfk_2;
ALTER TABLE discount_product DROP COLUMN vendor_id;
ALTER TABLE discount_product
ADD FOREIGN KEY (product_id) REFERENCES product(product_id);
ALTER TABLE discounts DROP FOREIGN KEY discounts_ibfk_1;
ALTER TABLE discounts DROP COLUMN vendor_id;
DROP TABLE vendor_product;

ALTER TABLE vendor_product
DROP COLUMN warranty_period;

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
	chat_id INT AUTO_INCREMENT PRIMARY KEY,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    text TEXT,
    images JSON,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (sender_id) REFERENCES accounts(account_id),
    FOREIGN KEY (receiver_id) REFERENCES  accounts(account_id)
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


SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE discount_product;
TRUNCATE TABLE discounts;
TRUNCATE TABLE orders;
TRUNCATE TABLE cart;
TRUNCATE TABLE product_colors;
TRUNCATE TABLE product_sizes;
TRUNCATE TABLE product;
TRUNCATE TABLE accounts;
SET FOREIGN_KEY_CHECKS = 1;

INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES
('Collin', 'Willimas', 'LunarDrift', 'SixSeven67!', 'reallyck2997@tempmail.com', 'admin'),
('Rob', 'Wiley', 'AtlasBloom', 'coffeeBreak99', 'neonwolf33@tempmail.com', 'admin'),
('Logan', 'Burkey', 'HexFrost', 'midnightDrive6', 'sunsetcoder19@tempmail.com', 'admin' );

SELECT * From accounts;

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

SELECT * FROM accounts;
