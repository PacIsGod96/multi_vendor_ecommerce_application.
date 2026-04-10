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