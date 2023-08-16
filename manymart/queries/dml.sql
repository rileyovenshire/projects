--------------------
-- Orders Page
--------------------

-- New Order
INSERT INTO Orders (order_id, customer_id, shipment_id, order_date) VALUES
(:order_idInput, :customer_idInput, :shipment_idInput, :order_dateInput);

-- View Order
SELECT * FROM Orders;
SELECT * FROM Customers

-- Delete Order
DELETE FROM Shipments where order_id = ?;
DELETE FROM Orders WHERE order_id = ?;

-- Update Order
UPDATE Orders SET customer_id = ?, shipment_id = ? WHERE order_id = ?;

--------------------
-- Shipments Page
--------------------

-- New Shipment
INSERT INTO Shipments (shipment_id, order_id, shipment_date, shipment_status) VALUES
(:shipment_idInput, :order_idInput, :shipment_dateInput, :shipment_statusInput);

-- Shipment Info
SELECT * FROM Shipments WHERE shipment_id = :shipment_idInput;

-- Update Shipment Date
UPDATE Shipments SET shipment_date = :shipment_dateInput;

-- Update Shipment Status
UPDATE Shipments SET shipment_status = :shipment_statusInput;

--------------------
-- Customers Page
--------------------

-- New Customer
INSERT INTO Customers (customer_id, first_name, last_name, email) VALUES
(:customer_idInput, :first_nameInput, :last_nameInput, :emailInput);

-- Get Customer Info
SELECT * FROM Customers WHERE full_name = :full_nameInput;

-- Change Email
UPDATE Customers SET email = ? WHERE Customers.last_name = ?;

-- See Orders
SELECT * FROM Orders;

-- Delete Customer
DELETE FROM Shipments where order_id = ?;
DELETE FROM Orders WHERE order_id = ?;

--------------------
-- Item Page
--------------------

-- New Item
INSERT INTO Items (item_id, item_name, item_price, item_quantity, department_id) VALUES
(:item_idInput, :item_nameInput, :item_priceInput, :item_quantityInput, :department_idInput);

-- Update Item Price and Quantity
UPDATE Orders SET customer_id = ?, shipment_id = ? WHERE order_id = ?;

--------------------
-- Department Page
--------------------

-- New Department
INSERT INTO Departments (department_id, department_name, dept_quantity) VALUES
(:department_idInput, :department_nameInput, :dept_quantityInput);

-- Department Full Info
SELECT * FROM Departments

-- See all items in one department
SELECT item_name FROM Items WHERE department_id = ?;

--------------------
-- OrderItems Page
--------------------
-- Join Orders and Items to see full table
SELECT oi.order_item_id, o.order_id, i.item_id
        FROM OrderItems oi
        INNER JOIN Orders o ON oi.order_id = o.order_id
        INNER JOIN Items i ON oi.item_id = i.item_id;

-- Add OrderItems when Order is created
INSERT INTO OrderItems (order_id, item_id) VALUES ('${data.orderID}', '${data.itemID}')



