CREATE DATABASE IF NOT EXISTS bakery_db;
USE bakery_db;

CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    price DECIMAL(10,2) NOT NULL,
    cost_price DECIMAL(10,2) DEFAULT 0,
    stock INT DEFAULT 0,
    expiry_date DATE
);

CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    quantity DECIMAL(10,2),
    unit VARCHAR(20),
    last_updated DATE
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    order_date DATE NOT NULL,
    total_amount DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS order_items (
    item_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    product_id INT,
    quantity INT,
    price DECIMAL(10,2),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

INSERT INTO products (name, category, price, cost_price, stock, expiry_date) VALUES
('Chocolate Cake', 'Cakes', 450.00, 200.00, 10, '2025-05-01'),
('Butter Croissant', 'Pastries', 60.00, 25.00, 20, '2025-04-15'),
('Blueberry Muffin', 'Muffins', 80.00, 35.00, 15, '2025-04-12'),
('Sourdough Bread', 'Bread', 120.00, 55.00, 8, '2025-04-13');

INSERT INTO inventory (name, quantity, unit, last_updated) VALUES
('Flour', 25.0, 'kg', '2025-04-01'),
('Sugar', 10.0, 'kg', '2025-04-01'),
('Butter', 5.0, 'kg', '2025-04-01'),
('Milk', 15.0, 'litres', '2025-04-01'),
('Eggs', 100.0, 'pieces', '2025-04-01');
