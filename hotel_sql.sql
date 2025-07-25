CREATE DATABASE hotel_menu;

USE hotel_menu;

CREATE TABLE menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    price DECIMAL(10,2),
    category VARCHAR(50)
);

CREATE TABLE tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number VARCHAR(10)
);
INSERT INTO menu_items (name, price, category) VALUES 
('Paneer Butter Masala', 250.00, 'Main Course'),
('Butter Naan', 40.00, 'Breads'),
('Masala Dosa', 100.00, 'South Indian');
