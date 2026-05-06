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
    name VARCHAR(50) NOT NULL
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

SELECT * From accounts;

SELECT * FROM product;

- #5: "?" will be new value being checked - 
INSERT INTO accounts (first_name, last_name, username, password, email_address, role) VALUES ('user', 'create', 'createUser', 'pw', 'email', 'user');
INSERT INTO product (name, description, images) VALUES ('product', 'description', 'image');
INSERT INTO vendor_product (vendor_id, product_id, price, available_inventory) VALUES (8, 69, 20, 200);
UPDATE product SET name = 'product1', description = 'new', images = 'image1' WHERE product_id = 1;
UPDATE vendor_product SET price = 70, available_inventory = 180 WHERE vendor_id = 8 AND product_id = 69;
DELETE FROM product WHERE product_id = 69;
INSERT INTO cart (account_id, product_id, quantity) VALUES (1, 69, 4);
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
DELETE FROM wishlist WHERE wishlist_id = 1;
INSERT INTO orders (account_id, date, status, total_price) VALUES (?, CURDATE(), 'pending', ?);
UPDATE orders SET status = 'confirmed' WHERE order_id = 1;
UPDATE orders SET status = ? WHERE order_id = 1;
INSERT INTO review (name, description, stars, date, account_id, product_id) VALUES ("review", "description", 5, CURDATE(), 1, 69);
UPDATE review SET description = 'desc', stars = 4 WHERE review_id = 1;
DELETE FROM review WHERE review_id = ?;
INSERT INTO returns (name, description, date, status, account_id) VALUES ('name', 'desc', CURDATE(), 'pending', 1);
UPDATE returns SET status = 'pending' WHERE return_id = 1;  
INSERT INTO chat (text, images, account_id) VALUES ('text', 'img', 1);
DELETE FROM chat WHERE chat_id = 1;

-- Rob  5/4: Run 183 - 195 --
SET SQL_SAFE_UPDATES = 0;
ALTER TABLE product DROP COLUMN description;
CREATE TABLE product_images (
    image_id INT AUTO_INCREMENT PRIMARY KEY,
    product_id INT,
    image_path VARCHAR(255)
);
ALTER TABLE product DROP COLUMN images;
SET SQL_SAFE_UPDATES = 1;
ALTER TABLE product ADD COLUMN vendor VARCHAR(40) NOT NULL;
UPDATE product SET vendor = "Drip Market" WHERE product_id = 1;
UPDATE product_images SET image_path = "DripPlazaTee3.png" WHERE image_id = 2;
UPDATE product_images SET image_path = CONCAT('Images/', image_path) WHERE image_path NOT LIKE 'Images/%';
ALTER TABLE product ADD COLUMN price INT NOT NULL;

SELECT * FROM product;
SELECT * FROM product_colors;
SELECT * FROM product_images;
SELECT * FROM product_sizes;
DELETE FROM product_images WHERE product_id = 2;

SELECT * FROM accounts;
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


-- --Logan

