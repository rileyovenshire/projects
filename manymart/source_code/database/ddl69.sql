-- Group: Loop 69
-- Members: Riley Ovenshire, Triston Osborn

-- Trigger source: https://www.javatpoint.com/mysql-create-trigger


-- Disable foreign key checks to allow for table creation
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Table creation

CREATE OR REPLACE TABLE Customers (
    customer_id int unique NOT NULL AUTO_INCREMENT,
    first_name varchar(50) NOT NULL,
    last_name varchar(50) NOT NULL,
    email varchar(62) NOT NULL,
    PRIMARY KEY (customer_id)
);

INSERT INTO Customers (first_name, last_name, email) 
VALUES ('Method', 'Man', 'methodman@gmail.com'),
("Eazy", "E", "ez_e@icloud.com"),
("Mos", "Def", "mosdef@yahoo.com"),
("Notorious", "BIG", "biggie@gmail.com"),
("Tupac", "Shakur", "tupac_shakur@icloud.com");


CREATE OR REPLACE TABLE Departments (
    department_id int unique NOT NULL AUTO_INCREMENT,
    department_name varchar(30) NOT NULL,
    dept_quantity int NOT NULL,
    PRIMARY KEY (department_id)
);

INSERT INTO Departments (department_name, dept_quantity) 
VALUES ("Electronics", 10),
("Clothing", 20),
("Music", 30),
("Books", 40);

CREATE OR REPLACE TABLE Items (
    item_id int unique NOT NULL AUTO_INCREMENT,
    item_name varchar(60) NOT NULL,
    item_price decimal(10,2) NOT NULL,
    item_quantity int NOT NULL,
    department_id int,
    PRIMARY KEY (item_id),
    FOREIGN KEY (department_id) REFERENCES Departments(department_id)
);

INSERT INTO Items (item_name, item_price, item_quantity, department_id)
VALUES ('Samsung 65" OLED', 1700.00, 10, 1),
("Nike Hoodie", 40.00, 20, 2),
("Enter the Wu-Tang (36 Chambers) CD", 10.00, 30, 3),
("Gravity's Rainbow", 18.00, 40, 4);

CREATE OR REPLACE TABLE Orders (
    order_id int unique NOT NULL AUTO_INCREMENT,
    customer_id int,
    shipment_id int,
    order_date date NOT NULL,
    PRIMARY KEY (order_id),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (shipment_id) REFERENCES Shipments(shipment_id)
);

INSERT INTO Orders (customer_id, shipment_id, order_date) 
VALUES (1, 1, "2019-01-01"),
(2, 2, "2019-01-02"),
(3, 3, "2019-01-03");

CREATE OR REPLACE TABLE Shipments (
    shipment_id int unique NOT NULL AUTO_INCREMENT,
    order_id int,
    shipment_date date NOT NULL,
    shipment_status boolean NOT NULL,
    PRIMARY KEY (shipment_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) on update cascade on delete cascade
);


INSERT INTO Shipments (order_id, shipment_date, shipment_status) 
VALUES (1, "2019-01-01", 1),
(2, "2019-01-02", 1),
(3, "2019-01-03", 1),
(4, "2019-01-04", 1);


-- Junction table
CREATE OR REPLACE TABLE OrderItems (
    order_item_id int unique NOT NULL AUTO_INCREMENT,
    order_id int,
    item_id int,
    PRIMARY KEY (order_id, item_id),
    -- need to delete order items when order is deleted
    FOREIGN KEY (order_id) REFERENCES Orders(order_id) on delete cascade,
    FOREIGN KEY (item_id) REFERENCES Items(item_id)
);

INSERT INTO OrderItems (order_id, item_id) 
VALUES (1, 1),
(1, 4),
(2, 2),
(2, 3),
(3, 3);

DELIMITER //

CREATE TRIGGER CreateShipmentAfterOrder
AFTER INSERT ON Orders FOR EACH ROW
BEGIN
    INSERT INTO Shipments (order_id, shipment_date, shipment_status)
    VALUES (NEW.order_id, CURDATE(), 0);
END;
//

DELIMITER ;

-- DELIMITER //

--     CREATE PROCEDURE CreateOrderWithShipment(IN orderDate date, IN customerID int)
--     BEGIN
--         -- Declare variable
--         DECLARE temp_id INT;

--         -- Insert a new Order
--         INSERT INTO Orders (customer_id, order_date) VALUES (customerID, orderDate);
--         SET temp_id = LAST_INSERT_ID(); -- Save the Order's primary key

--         -- Insert a new Shipment
--         INSERT INTO Shipments (order_id, shipment_date, shipment_status) VALUES (temp_id, CURDATE(), 0);

--         -- Update the foreign key in Orders with the generated primary key of the Shipment
--         UPDATE Orders SET shipment_id = LAST_INSERT_ID() WHERE order_id = temp_id;
--     END;

-- //
-- DELIMITER ;

-- Enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;
COMMIT;